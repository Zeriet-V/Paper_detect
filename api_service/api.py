#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论文格式检测系统 - REST API 接口

功能：
1. 接收Word文档上传
2. 执行论文格式检测
3. 返回检测报告（JSON格式）
4. 返回带批注的文档

端点：
- POST /api/detect - 上传文档并执行检测
- GET /api/health - 健康检查
- GET /api/download/{task_id}/report - 下载文本报告
- GET /api/download/{task_id}/annotated - 下载带批注的文档
"""

import os
import sys
import json
import uuid
import shutil
from typing import Optional
from datetime import datetime
from pathlib import Path

# 添加父目录到路径，以便导入检测模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 导入检测系统
from run_all_detections import (
    import_detection_modules,
    run_all_detections,
    generate_comprehensive_report,
    save_report_to_file,
    create_document_copy
)

# 创建FastAPI应用
app = FastAPI(
    title="论文格式检测系统API",
    description="提供论文Word文档格式检测服务",
    version="1.0.0"
)

# 配置CORS（允许跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置目录
UPLOAD_DIR = Path("uploads")
RESULT_DIR = Path("results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

# 任务存储（生产环境应使用数据库）
tasks = {}

# 预加载检测模块
detection_functions = None


class DetectionResponse(BaseModel):
    """检测响应模型"""
    task_id: str
    status: str
    message: str
    created_at: str


class TaskStatus(BaseModel):
    """任务状态模型"""
    task_id: str
    status: str  # pending, processing, completed, failed
    created_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None
    result: Optional[dict] = None


class DetectionResult(BaseModel):
    """检测结果模型"""
    total_checks: int
    passed_checks: int
    failed_checks: int
    pass_rate: float
    modules: dict
    report_url: Optional[str] = None
    annotated_doc_url: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """应用启动时加载检测模块"""
    global detection_functions
    print("正在加载检测模块...")
    try:
        detection_functions = import_detection_modules()
        print("✓ 所有检测模块加载成功")
    except Exception as e:
        print(f"✗ 加载检测模块失败: {e}")
        raise


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "论文格式检测系统API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "detect": "POST /api/detect",
            "status": "GET /api/status/{task_id}",
            "report": "GET /api/download/{task_id}/report",
            "annotated": "GET /api/download/{task_id}/annotated"
        }
    }


@app.get("/api/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "detection_modules": len(detection_functions) if detection_functions else 0
    }


def process_detection(task_id: str, file_path: str):
    """
    后台处理检测任务
    
    参数：
        task_id: 任务ID
        file_path: 上传的文件路径
    """
    try:
        # 更新任务状态
        tasks[task_id]["status"] = "processing"
        
        # 执行检测
        all_reports = run_all_detections(file_path, detection_functions)
        
        # 生成报告
        report_text = generate_comprehensive_report(all_reports)
        
        # 保存报告文件
        report_filename = f"{task_id}_report.txt"
        report_path = RESULT_DIR / report_filename
        save_report_to_file(report_text, str(report_path))
        
        # 创建带批注的文档
        annotated_filename = f"{task_id}_annotated.docx"
        annotated_path = RESULT_DIR / annotated_filename
        
        # 创建文档副本并添加批注
        temp_copy = create_document_copy(file_path)
        if temp_copy:
            # 导入批注功能
            from run_all_detections import (
                parse_issues_from_reports,
                find_paragraph_by_keyword,
                find_paragraph_by_index,
                add_comment_to_paragraph
            )
            from docx import Document
            
            # 解析问题并添加批注
            doc = Document(temp_copy)
            issues = parse_issues_from_reports(all_reports)
            
            for issue in issues:
                locate_method = issue['locate_method']
                locate_data = issue['locate_data']
                messages = issue['messages']
                comment_text = f"【{issue['module']} - {issue['section']}】\n" + "\n".join(messages)
                
                # 定位段落
                paragraph = None
                if locate_method == 'keyword':
                    paragraph = find_paragraph_by_keyword(doc, locate_data)
                elif locate_method == 'index':
                    paragraph = find_paragraph_by_index(doc, locate_data)
                
                # 添加批注
                if paragraph:
                    add_comment_to_paragraph(doc, paragraph, comment_text)
            
            # 保存带批注的文档
            doc.save(str(annotated_path))
            # 删除临时副本
            if os.path.exists(temp_copy):
                os.remove(temp_copy)
        
        # 计算统计信息
        total_checks = 0
        passed_checks = 0
        
        for module_name, report in all_reports.items():
            if report.get('error', False):
                continue
            
            for key, value in report.items():
                if isinstance(value, dict) and 'ok' in value:
                    total_checks += 1
                    if value.get('ok', False):
                        passed_checks += 1
        
        failed_checks = total_checks - passed_checks
        pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        # 更新任务状态
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        tasks[task_id]["result"] = {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "pass_rate": round(pass_rate, 2),
            "modules": all_reports,
            "report_url": f"/api/download/{task_id}/report",
            "annotated_doc_url": f"/api/download/{task_id}/annotated"
        }
        
    except Exception as e:
        # 更新任务状态为失败
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["completed_at"] = datetime.now().isoformat()
        tasks[task_id]["error"] = str(e)
        print(f"检测任务失败: {e}")


@app.post("/api/detect", response_model=DetectionResponse)
async def detect_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    上传Word文档并执行检测
    
    参数：
        file: 上传的Word文档（.docx格式）
    
    返回：
        任务ID和状态信息
    """
    # 验证文件类型
    if not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="仅支持.docx格式的Word文档"
        )
    
    # 生成任务ID
    task_id = str(uuid.uuid4())
    
    # 保存上传的文件
    upload_filename = f"{task_id}_{file.filename}"
    upload_path = UPLOAD_DIR / upload_filename
    
    try:
        with open(upload_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件保存失败: {str(e)}"
        )
    
    # 创建任务记录
    tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "filename": file.filename,
        "file_path": str(upload_path)
    }
    
    # 添加后台任务
    background_tasks.add_task(process_detection, task_id, str(upload_path))
    
    return DetectionResponse(
        task_id=task_id,
        status="pending",
        message="检测任务已创建，正在处理中...",
        created_at=tasks[task_id]["created_at"]
    )


@app.get("/api/status/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """
    查询任务状态
    
    参数：
        task_id: 任务ID
    
    返回：
        任务状态信息
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = tasks[task_id]
    
    return TaskStatus(
        task_id=task_id,
        status=task["status"],
        created_at=task["created_at"],
        completed_at=task.get("completed_at"),
        error=task.get("error"),
        result=task.get("result")
    )


@app.get("/api/download/{task_id}/report")
async def download_report(task_id: str):
    """
    下载文本报告
    
    参数：
        task_id: 任务ID
    
    返回：
        文本报告文件
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")
    
    report_path = RESULT_DIR / f"{task_id}_report.txt"
    
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="报告文件不存在")
    
    return FileResponse(
        path=str(report_path),
        filename=f"report_{task_id}.txt",
        media_type="text/plain"
    )


@app.get("/api/download/{task_id}/annotated")
async def download_annotated_document(task_id: str):
    """
    下载带批注的文档
    
    参数：
        task_id: 任务ID
    
    返回：
        带批注的Word文档
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = tasks[task_id]
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="任务尚未完成")
    
    annotated_path = RESULT_DIR / f"{task_id}_annotated.docx"
    
    if not annotated_path.exists():
        raise HTTPException(status_code=404, detail="带批注的文档不存在")
    
    return FileResponse(
        path=str(annotated_path),
        filename=f"annotated_{task_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    删除任务及相关文件
    
    参数：
        task_id: 任务ID
    
    返回：
        删除结果
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = tasks[task_id]
    
    # 删除相关文件
    files_to_delete = [
        task.get("file_path"),
        str(RESULT_DIR / f"{task_id}_report.txt"),
        str(RESULT_DIR / f"{task_id}_annotated.docx")
    ]
    
    for file_path in files_to_delete:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"删除文件失败: {file_path}, {e}")
    
    # 删除任务记录
    del tasks[task_id]
    
    return {"message": "任务已删除", "task_id": task_id}


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("论文格式检测系统 API 服务")
    print("=" * 60)
    print("启动服务器...")
    print("API文档: http://localhost:8000/docs")
    print("=" * 60)
    
    # 使用导入字符串格式以支持reload功能
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
