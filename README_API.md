# 论文格式检测系统 - API服务

## 📋 项目说明

本项目已将论文格式检测功能封装为RESTful API服务，所有API相关文件已整理到 `api_service/` 目录中。

## 📂 目录结构

```
paper_detect/
├── api_service/              # ⭐ API服务目录（所有API文件）
│   ├── api.py               # API服务主文件
│   ├── requirements.txt     # 依赖包
│   ├── start_api.bat       # 启动脚本
│   ├── web_demo.html       # Web测试界面
│   ├── test_api_client.py  # 测试客户端
│   ├── 集成示例.py          # 集成代码示例
│   ├── API_README.md       # API详细文档
│   ├── 快速开始.md         # 快速入门
│   ├── API使用总览.md      # 使用总览
│   └── README.md           # API目录说明
│
├── paper_detect/            # 检测模块（核心逻辑）
│   ├── Title_detect.py
│   ├── Abstract_detect.py
│   ├── Keywords_detect.py
│   ├── Content_detect.py
│   ├── Formula_detect.py
│   └── Table_detect.py
│
├── templates/               # 检测规则配置
│   ├── Title.json
│   ├── Abstract.json
│   ├── Keywords.json
│   ├── Content.json
│   ├── Formula.json
│   └── Table.json
│
├── template/                # 测试文档
│   └── test.docx
│
└── run_all_detections.py    # 命令行检测工具（原始工具）
```

## 🚀 两种使用方式

### 方式1：API服务（推荐，供系统集成）

**进入API目录并启动服务：**
```bash
cd api_service
start_api.bat
```

或者：
```bash
cd api_service
pip install -r requirements.txt
python api.py
```

服务地址：http://localhost:8000

**使用Web界面测试：**
- 打开 `api_service/web_demo.html`

**通过API调用：**
```python
import requests

files = {"file": open("paper.docx", "rb")}
response = requests.post("http://localhost:8000/api/detect", files=files)
task_id = response.json()["task_id"]
```

详细文档：查看 `api_service/API_README.md`

### 方式2：命令行工具（原始方式）

**在项目根目录运行：**
```bash
python run_all_detections.py template/test.docx
```

生成结果：
- `test_report.txt` - 文本报告
- `test_annotated.docx` - 带批注的文档

## 📚 API文档

进入 `api_service/` 目录查看详细文档：

| 文档 | 说明 |
|------|------|
| `README.md` | API目录说明 |
| `快速开始.md` | 3步快速上手 |
| `API使用总览.md` | 整体使用说明 |
| `API_README.md` | 完整API接口文档 |
| `集成示例.py` | 系统集成代码示例 |

## 🎯 快速开始

**第1步**：进入API目录
```bash
cd api_service
```

**第2步**：启动服务
```bash
start_api.bat
```

**第3步**：测试
- 打开 `web_demo.html` 或
- 运行 `python test_api_client.py ../template/test.docx` 或
- 访问 http://localhost:8000/docs

## 💡 适用场景

### 使用API服务
- ✅ 需要集成到其他系统（如论文提交系统）
- ✅ 需要远程调用
- ✅ 需要批量处理
- ✅ 需要Web界面

### 使用命令行工具
- ✅ 单机使用
- ✅ 简单快速
- ✅ 不需要服务器

## 🔧 API核心功能

- 📤 上传Word文档
- 🔍 自动格式检测
- 📊 返回JSON结果
- 📄 下载文本报告
- 📝 下载带批注文档
- 🌐 Web测试界面

## 📞 技术支持

- API文档：`api_service/API_README.md`
- 在线文档：http://localhost:8000/docs（启动服务后访问）
- 集成示例：`api_service/集成示例.py`

---

**建议**：如需集成到系统中，请查看 `api_service/` 目录下的文档开始使用。
