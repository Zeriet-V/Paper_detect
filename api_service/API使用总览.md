# 论文格式检测系统 - API使用总览

## 📋 项目简介

已成功将论文格式检测系统转换为API服务，支持以下功能：
- ✅ RESTful API接口
- ✅ 文件上传和异步处理
- ✅ 生成JSON格式检测结果
- ✅ 下载文本报告
- ✅ 下载带批注的文档
- ✅ Web测试界面
- ✅ Python客户端示例

## 🎯 三步开始使用

### 第1步：启动API服务

**方式A - 使用启动脚本（推荐）：**
```bash
# 双击运行
start_api.bat
```

**方式B - 命令行：**
```bash
# 安装依赖（首次）
pip install -r requirements.txt

# 启动服务
python api.py
```

服务地址：http://localhost:8000

### 第2步：选择使用方式

**🌐 方式1：Web界面（最简单）**
- 打开 `web_demo.html` 文件
- 拖拽Word文档上传
- 查看检测结果并下载

**🔧 方式2：Python客户端**
```bash
python test_api_client.py template/test.docx
```

**💻 方式3：集成到系统**
```python
from 集成示例 import PaperDetectionService

service = PaperDetectionService()
result = service.detect_and_wait("paper.docx")
print(f"通过率: {result['pass_rate']}%")
```

### 第3步：查看结果

检测完成后可以：
- 查看JSON格式的检测结果
- 下载详细的文本报告
- 下载带批注标记的Word文档

## 📁 文件清单

| 文件 | 说明 | 用途 |
|------|------|------|
| `api.py` | API服务主文件 | 启动服务 |
| `start_api.bat` | 启动脚本 | 一键启动（Windows） |
| `requirements.txt` | 依赖列表 | 安装依赖 |
| `web_demo.html` | Web测试界面 | 可视化测试 |
| `test_api_client.py` | Python测试客户端 | 命令行测试 |
| `集成示例.py` | 集成代码示例 | 系统集成参考 |
| `API_README.md` | 详细API文档 | API接口说明 |
| `快速开始.md` | 快速入门 | 新手指南 |
| `API使用总览.md` | 本文件 | 整体概览 |

## 🔌 API端点

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| POST | `/api/detect` | 上传文档检测 |
| GET | `/api/status/{task_id}` | 查询任务状态 |
| GET | `/api/download/{task_id}/report` | 下载文本报告 |
| GET | `/api/download/{task_id}/annotated` | 下载带批注文档 |
| DELETE | `/api/tasks/{task_id}` | 删除任务 |

详细说明见：[API_README.md](API_README.md)

## 💡 使用场景

### 场景1：在线论文提交系统
学生提交论文时自动进行格式检测，不符合要求则提示修改。

```python
# 集成到提交系统
from 集成示例 import PaperDetectionService

service = PaperDetectionService("http://your-api-server:8000")
result = service.detect_and_wait(paper_path)

if result['pass_rate'] >= 80:
    # 允许提交
    accept_submission()
else:
    # 要求修改
    reject_with_feedback(result)
```

### 场景2：论文管理系统
批量检测已提交的论文，生成统计报告。

```python
# 批量处理
documents = get_all_papers()
for doc in documents:
    task_id = service.upload_document(doc)
    # 异步处理...
```

### 场景3：单机工具
直接使用Web界面或命令行工具进行检测。

```bash
# 命令行
python test_api_client.py my_paper.docx

# 或使用原始工具
python run_all_detections.py my_paper.docx
```

## 🔐 生产环境部署建议

### 1. 安全性
- 添加API认证（JWT Token或API Key）
- 启用HTTPS
- 限制文件大小（建议10MB以内）
- 添加访问频率限制

### 2. 性能优化
- 使用任务队列（Celery + Redis）
- 文件存储使用OSS（阿里云OSS/AWS S3）
- 使用数据库持久化任务信息
- 添加缓存机制

### 3. 监控和日志
- 添加日志记录
- 监控API性能和错误率
- 设置告警机制

### 4. Docker部署
```dockerfile
# 示例Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "api.py"]
```

### 5. 负载均衡
多实例部署 + Nginx反向代理

## 📊 检测结果格式

```json
{
  "total_checks": 50,
  "passed_checks": 45,
  "failed_checks": 5,
  "pass_rate": 90.0,
  "modules": {
    "Title": {
      "title_format": {"ok": true, "messages": []},
      "author_info": {"ok": false, "messages": ["作者格式错误"]}
    },
    "Abstract": {...},
    "Keywords": {...},
    "Content": {...},
    "Formula": {...},
    "Table": {...}
  }
}
```

## 🎓 学习资源

1. **快速上手**：`快速开始.md`
2. **API文档**：`API_README.md` 或访问 http://localhost:8000/docs
3. **集成示例**：`集成示例.py`
4. **原理说明**：查看各检测模块源码（`paper_detect/`目录）

## ❓ 常见问题

**Q: 如何修改端口？**
A: 编辑 `api.py` 最后一行，修改 `port=8000`

**Q: 如何允许远程访问？**
A: 确保防火墙开放端口，API已默认监听 `0.0.0.0`

**Q: 检测太慢怎么办？**
A: 检测是CPU密集型任务，考虑：
- 使用更强的服务器
- 部署多个实例
- 使用任务队列分布式处理

**Q: 如何自定义检测规则？**
A: 修改 `templates/` 目录下的JSON配置文件

**Q: 能否同时检测多个文档？**
A: 可以！API支持并发处理，每个文档会创建独立的任务

## 📞 技术支持

- 📖 查看文档：`API_README.md`
- 🌐 在线文档：http://localhost:8000/docs
- 💻 示例代码：`集成示例.py`
- 🔧 测试工具：`test_api_client.py`

## 🚀 下一步

1. ✅ 启动服务：`python api.py`
2. ✅ 测试接口：打开 `web_demo.html`
3. ✅ 查看文档：http://localhost:8000/docs
4. ✅ 集成到系统：参考 `集成示例.py`

---

**祝使用愉快！🎉**

如有问题，请查看详细文档或联系开发团队。
