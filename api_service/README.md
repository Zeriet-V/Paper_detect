# API服务目录

本目录包含论文格式检测系统的API服务相关文件。

## 📁 目录结构

```
api_service/
├── api.py                    # API服务主文件
├── requirements.txt          # Python依赖包
├── start_api.bat            # 启动脚本（Windows）
├── web_demo.html            # Web测试界面
├── test_api_client.py       # Python测试客户端
├── 集成示例.py               # 系统集成代码示例
├── test_import.py           # 导入测试脚本
├── API_README.md            # 详细API文档
├── 快速开始.md               # 快速入门指南
├── API使用总览.md            # 使用总览
└── README.md                # 本文件
```

## 🚀 快速启动

### 方式1：使用启动脚本（推荐）

```bash
# 在本目录下运行
start_api.bat
```

### 方式2：命令行启动

```bash
# 1. 安装依赖（首次使用）
pip install -r requirements.txt

# 2. 启动服务
python api.py
```

服务将在 http://localhost:8000 启动

## 📖 文档说明

| 文档 | 内容 |
|------|------|
| `快速开始.md` | 新手入门，3步开始使用 |
| `API使用总览.md` | 整体使用说明和场景 |
| `API_README.md` | 完整的API接口文档 |

## 🧪 测试方式

### 1. Web界面测试
直接用浏览器打开 `web_demo.html`，拖拽Word文档上传测试。

### 2. Python客户端测试
```bash
python test_api_client.py ../template/test.docx
```

### 3. 集成测试
```bash
python 集成示例.py
```

## 🌐 访问地址

启动服务后：
- API服务: http://localhost:8000
- 接口文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc

## 📝 快速使用示例

```python
import requests

# 上传文档
files = {"file": open("paper.docx", "rb")}
response = requests.post("http://localhost:8000/api/detect", files=files)
task_id = response.json()["task_id"]

# 查询状态
status = requests.get(f"http://localhost:8000/api/status/{task_id}")
print(status.json())
```

详细示例请查看 `集成示例.py`

## ⚙️ 配置说明

### 修改端口
编辑 `api.py` 最后一行：
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # 改为8080端口
```

### 文件存储路径
默认创建两个目录：
- `uploads/` - 上传的文档
- `results/` - 检测结果

## 💡 注意事项

1. API服务需要访问父目录的检测模块（`../run_all_detections.py`）
2. 示例文件路径使用相对路径（`../template/test.docx`）
3. 生成的结果文件存储在本地，建议定期清理

## 🔗 相关文件

API服务依赖项目根目录下的以下模块：
- `run_all_detections.py` - 核心检测逻辑
- `paper_detect/` - 检测模块
  - Title_detect.py
  - Abstract_detect.py
  - Keywords_detect.py
  - Content_detect.py
  - Formula_detect.py
  - Table_detect.py
- `templates/` - 检测规则配置

## 📞 获取帮助

- 查看 `快速开始.md` 了解基本使用
- 查看 `API_README.md` 了解详细API
- 查看 `集成示例.py` 了解系统集成

祝使用愉快！🎉
