#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统集成示例

演示如何将论文格式检测API集成到现有系统中
"""

import requests
import time
from typing import Optional, Dict


class PaperDetectionService:
    """
    论文检测服务封装类
    
    使用示例：
        service = PaperDetectionService("http://your-api-server:8000")
        result = service.detect_and_wait("paper.docx")
        print(f"检测通过率: {result['pass_rate']}%")
    """
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        初始化服务
        
        Args:
            api_base_url: API服务地址
        """
        self.api_base_url = api_base_url.rstrip('/')
    
    def check_health(self) -> bool:
        """
        检查服务健康状态
        
        Returns:
            True: 服务正常
            False: 服务异常
        """
        try:
            response = requests.get(f"{self.api_base_url}/api/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def upload_document(self, file_path: str) -> Optional[str]:
        """
        上传文档并创建检测任务
        
        Args:
            file_path: 文档路径
            
        Returns:
            任务ID，失败返回None
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.api_base_url}/api/detect",
                    files=files,
                    timeout=30
                )
                response.raise_for_status()
                return response.json()['task_id']
        except Exception as e:
            print(f"上传失败: {e}")
            return None
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务状态字典，失败返回None
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/api/status/{task_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取状态失败: {e}")
            return None
    
    def wait_for_completion(
        self, 
        task_id: str, 
        timeout: int = 300,
        callback=None
    ) -> Optional[Dict]:
        """
        等待任务完成
        
        Args:
            task_id: 任务ID
            timeout: 超时时间（秒）
            callback: 进度回调函数
            
        Returns:
            检测结果，失败返回None
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            
            if not status:
                return None
            
            # 回调通知
            if callback:
                callback(status['status'])
            
            if status['status'] == 'completed':
                return status['result']
            elif status['status'] == 'failed':
                print(f"检测失败: {status.get('error', '未知错误')}")
                return None
            
            time.sleep(2)
        
        print("等待超时")
        return None
    
    def download_report(self, task_id: str, output_path: str) -> bool:
        """
        下载文本报告
        
        Args:
            task_id: 任务ID
            output_path: 输出路径
            
        Returns:
            成功返回True
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/api/download/{task_id}/report",
                timeout=30
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"下载报告失败: {e}")
            return False
    
    def download_annotated_document(self, task_id: str, output_path: str) -> bool:
        """
        下载带批注的文档
        
        Args:
            task_id: 任务ID
            output_path: 输出路径
            
        Returns:
            成功返回True
        """
        try:
            response = requests.get(
                f"{self.api_base_url}/api/download/{task_id}/annotated",
                timeout=30
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"下载带批注文档失败: {e}")
            return False
    
    def detect_and_wait(
        self, 
        file_path: str,
        download_report_path: Optional[str] = None,
        download_annotated_path: Optional[str] = None
    ) -> Optional[Dict]:
        """
        一站式检测：上传、等待、下载
        
        Args:
            file_path: 待检测文档路径
            download_report_path: 报告保存路径（可选）
            download_annotated_path: 带批注文档保存路径（可选）
            
        Returns:
            检测结果字典
        """
        # 上传
        print(f"上传文档: {file_path}")
        task_id = self.upload_document(file_path)
        if not task_id:
            return None
        
        print(f"任务ID: {task_id}")
        
        # 等待完成
        print("等待检测完成...")
        result = self.wait_for_completion(
            task_id,
            callback=lambda s: print(f"状态: {s}", end='\r')
        )
        
        if not result:
            return None
        
        print(f"\n检测完成！")
        print(f"通过率: {result['pass_rate']}%")
        print(f"通过: {result['passed_checks']}/{result['total_checks']}")
        
        # 下载文件
        if download_report_path:
            print(f"下载报告: {download_report_path}")
            self.download_report(task_id, download_report_path)
        
        if download_annotated_path:
            print(f"下载带批注文档: {download_annotated_path}")
            self.download_annotated_document(task_id, download_annotated_path)
        
        return result


# ============================================================
# 使用示例
# ============================================================

def example_1_simple():
    """示例1：简单使用"""
    print("\n" + "=" * 60)
    print("示例1：简单使用")
    print("=" * 60)
    
    service = PaperDetectionService()
    
    # 检查服务
    if not service.check_health():
        print("❌ API服务不可用，请先启动服务")
        print("   运行: python api.py")
        return
    
    print("✓ API服务正常")
    
    # 检测文档
    result = service.detect_and_wait(
        "../template/test.docx",
        download_report_path="my_report.txt",
        download_annotated_path="my_annotated.docx"
    )
    
    if result:
        print("\n✅ 检测成功！")
    else:
        print("\n❌ 检测失败")


def example_2_detailed():
    """示例2：详细控制"""
    print("\n" + "=" * 60)
    print("示例2：详细控制流程")
    print("=" * 60)
    
    service = PaperDetectionService()
    
    # 1. 上传
    task_id = service.upload_document("../template/test.docx")
    if not task_id:
        print("上传失败")
        return
    
    print(f"✓ 上传成功，任务ID: {task_id}")
    
    # 2. 轮询状态
    while True:
        status = service.get_task_status(task_id)
        if not status:
            break
        
        print(f"状态: {status['status']}", end='\r')
        
        if status['status'] == 'completed':
            result = status['result']
            print(f"\n✓ 检测完成")
            print(f"  通过率: {result['pass_rate']}%")
            print(f"  总检测项: {result['total_checks']}")
            print(f"  通过项: {result['passed_checks']}")
            print(f"  失败项: {result['failed_checks']}")
            
            # 3. 下载结果
            service.download_report(task_id, "detailed_report.txt")
            service.download_annotated_document(task_id, "detailed_annotated.docx")
            break
        
        elif status['status'] == 'failed':
            print(f"\n✗ 检测失败: {status.get('error')}")
            break
        
        time.sleep(2)


def example_3_batch():
    """示例3：批量检测"""
    print("\n" + "=" * 60)
    print("示例3：批量检测多个文档")
    print("=" * 60)
    
    service = PaperDetectionService()
    
    # 假设有多个文档需要检测
    documents = [
        "doc1.docx",
        "doc2.docx",
        "doc3.docx"
    ]
    
    # 批量上传
    tasks = []
    for doc in documents:
        print(f"上传: {doc}")
        task_id = service.upload_document(doc)
        if task_id:
            tasks.append({'doc': doc, 'task_id': task_id})
    
    # 等待所有任务完成
    print(f"\n等待 {len(tasks)} 个任务完成...")
    
    results = []
    for task in tasks:
        print(f"\n处理: {task['doc']}")
        result = service.wait_for_completion(task['task_id'])
        if result:
            results.append({
                'document': task['doc'],
                'pass_rate': result['pass_rate'],
                'result': result
            })
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("批量检测结果汇总")
    print("=" * 60)
    for r in results:
        print(f"{r['document']}: {r['pass_rate']}%")


def example_4_integration():
    """示例4：集成到现有系统"""
    print("\n" + "=" * 60)
    print("示例4：集成到现有业务系统")
    print("=" * 60)
    
    # 模拟现有系统的业务流程
    class PaperSubmissionSystem:
        """论文提交系统"""
        
        def __init__(self):
            self.detection_service = PaperDetectionService()
        
        def submit_paper(self, user_id: str, paper_path: str):
            """
            提交论文并进行格式检测
            
            Returns:
                (是否通过, 检测结果)
            """
            print(f"用户 {user_id} 提交论文: {paper_path}")
            
            # 1. 检测格式
            print("正在进行格式检测...")
            result = self.detection_service.detect_and_wait(paper_path)
            
            if not result:
                print("❌ 检测失败")
                return False, None
            
            # 2. 判断是否通过
            pass_rate = result['pass_rate']
            passed = pass_rate >= 80  # 设定通过标准为80%
            
            # 3. 保存结果到数据库（这里仅示例）
            self.save_to_database(user_id, paper_path, result)
            
            # 4. 通知用户
            if passed:
                print(f"✅ 论文格式检测通过！通过率: {pass_rate}%")
                self.notify_user(user_id, "论文已提交成功", result)
            else:
                print(f"❌ 论文格式不符合要求，通过率: {pass_rate}%")
                self.notify_user(user_id, "请修改格式后重新提交", result)
            
            return passed, result
        
        def save_to_database(self, user_id, paper_path, result):
            """保存到数据库（示例）"""
            print(f"  [DB] 保存检测结果: user={user_id}, pass_rate={result['pass_rate']}")
        
        def notify_user(self, user_id, message, result):
            """通知用户（示例）"""
            print(f"  [通知] {user_id}: {message}")
    
    # 使用示例
    system = PaperSubmissionSystem()
    passed, result = system.submit_paper("user123", "../template/test.docx")


if __name__ == "__main__":
    print("=" * 60)
    print("论文格式检测系统 - 集成示例")
    print("=" * 60)
    print("\n请确保API服务已启动: python api.py")
    print("\n选择示例:")
    print("1. 简单使用")
    print("2. 详细控制")
    print("3. 批量检测")
    print("4. 系统集成")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == '1':
        example_1_simple()
    elif choice == '2':
        example_2_detailed()
    elif choice == '3':
        example_3_batch()
    elif choice == '4':
        example_4_integration()
    else:
        print("无效选项")
