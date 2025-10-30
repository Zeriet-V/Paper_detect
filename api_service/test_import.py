#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""测试API导入"""

try:
    print("测试导入API模块...")
    from api import app
    print("✓ API模块导入成功")
    
    print("\n测试导入检测模块...")
    from run_all_detections import import_detection_modules
    print("✓ 检测模块导入成功")
    
    print("\n测试FastAPI依赖...")
    import fastapi
    import uvicorn
    from pydantic import BaseModel
    print("✓ FastAPI依赖完整")
    
    print("\n所有测试通过！✓")
    
except Exception as e:
    print(f"\n✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()
