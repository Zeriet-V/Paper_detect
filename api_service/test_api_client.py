#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API测试客户端

用于测试论文格式检测系统API的功能
"""

import requests
import time
import sys
from pathlib import Path


class PaperDetectionAPIClient:
    """论文检测API客户端"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self):
        """健康检查"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"健康检查失败: {e}")
            return None
    
    def upload_document(self, file_path):
        """上传文档并创建检测任务"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
                response = requests.post(
                    f"{self.base_url}/api/detect",
                    files=files
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"上传失败: {e}")
            return None
    
    def get_task_status(self, task_id):
        """获取任务状态"""
        try:
            response = requests.get(f"{self.base_url}/api/status/{task_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取状态失败: {e}")
            return None
    
    def wait_for_completion(self, task_id, timeout=300, check_interval=2):
        """等待任务完成"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_task_status(task_id)
            
            if not status:
                return None
            
            if status['status'] == 'completed':
                return status
            elif status['status'] == 'failed':
                print(f"任务失败: {status.get('error', '未知错误')}")
                return None
            
            print(f"任务状态: {status['status']}...", end='\r')
            time.sleep(check_interval)
        
        print(f"\n超时：任务在{timeout}秒内未完成")
        return None
    
    def download_report(self, task_id, output_path):
        """下载文本报告"""
        try:
            response = requests.get(f"{self.base_url}/api/download/{task_id}/report")
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"下载报告失败: {e}")
            return False
    
    def download_annotated_document(self, task_id, output_path):
        """下载带批注的文档"""
        try:
            response = requests.get(f"{self.base_url}/api/download/{task_id}/annotated")
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return True
        except Exception as e:
            print(f"下载带批注文档失败: {e}")
            return False
    
    def delete_task(self, task_id):
        """删除任务"""
        try:
            response = requests.delete(f"{self.base_url}/api/tasks/{task_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"删除任务失败: {e}")
            return None


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python test_api_client.py <docx文件路径>")
        print("\n示例:")
        print("  python test_api_client.py ../template/test.docx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not Path(file_path).exists():
        print(f"错误: 文件不存在 - {file_path}")
        sys.exit(1)
    
    # 检查文件格式
    if not file_path.lower().endswith('.docx'):
        print("错误: 文件必须是.docx格式")
        sys.exit(1)
    
    print("=" * 60)
    print("论文格式检测系统 - API 测试客户端")
    print("=" * 60)
    
    # 创建客户端
    client = PaperDetectionAPIClient()
    
    # 1. 健康检查
    print("\n[1/5] 检查API服务状态...")
    health = client.health_check()
    if not health:
        print("❌ API服务不可用，请确保服务已启动")
        print("   启动命令: python api.py")
        sys.exit(1)
    
    print(f"✓ API服务正常运行")
    print(f"  - 状态: {health['status']}")
    print(f"  - 检测模块数: {health['detection_modules']}")
    
    # 2. 上传文档
    print(f"\n[2/5] 上传文档: {file_path}")
    result = client.upload_document(file_path)
    if not result:
        print("❌ 上传失败")
        sys.exit(1)
    
    task_id = result['task_id']
    print(f"✓ 上传成功")
    print(f"  - 任务ID: {task_id}")
    print(f"  - 状态: {result['status']}")
    
    # 3. 等待检测完成
    print(f"\n[3/5] 等待检测完成...")
    status = client.wait_for_completion(task_id)
    if not status:
        print("\n❌ 检测失败或超时")
        sys.exit(1)
    
    print("\n✓ 检测完成")
    
    # 显示结果
    result_data = status['result']
    print(f"\n检测结果:")
    print(f"  - 总检测项: {result_data['total_checks']}")
    print(f"  - 通过项: {result_data['passed_checks']}")
    print(f"  - 失败项: {result_data['failed_checks']}")
    print(f"  - 通过率: {result_data['pass_rate']}%")
    
    # 4. 下载报告
    print(f"\n[4/5] 下载检测报告...")
    report_path = f"test_report_{task_id}.txt"
    if client.download_report(task_id, report_path):
        print(f"✓ 报告已保存到: {report_path}")
    else:
        print("❌ 下载报告失败")
    
    # 5. 下载带批注的文档
    print(f"\n[5/5] 下载带批注的文档...")
    annotated_path = f"test_annotated_{task_id}.docx"
    if client.download_annotated_document(task_id, annotated_path):
        print(f"✓ 带批注文档已保存到: {annotated_path}")
    else:
        print("❌ 下载带批注文档失败")
    
    # 询问是否删除任务
    print(f"\n" + "=" * 60)
    delete = input("是否删除任务? (y/n): ").strip().lower()
    if delete == 'y':
        if client.delete_task(task_id):
            print("✓ 任务已删除")
        else:
            print("❌ 删除任务失败")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
