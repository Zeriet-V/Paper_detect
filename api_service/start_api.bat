@echo off
chcp 65001 >nul
echo ========================================
echo 论文格式检测系统 - API服务启动脚本
echo ========================================
echo.

echo [1/2] 检查依赖...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 未安装依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 安装依赖失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo ✓ 依赖已安装
)

echo.
echo [2/2] 启动API服务...
echo.
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo Web测试: file:///%~dp0web_demo.html
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python api.py

pause
