# 论文格式检测系统 - API接口文档

## 概述

本API提供论文Word文档格式检测服务，支持以下功能：
- 上传Word文档（.docx格式）
- 自动检测论文格式规范
- 生成详细检测报告
- 返回带批注的文档

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python api.py
```

服务将在 `http://localhost:8000` 启动

### 3. 访问API文档

浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 1. 健康检查

**GET** `/api/health`

检查API服务状态

**响应示例：**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00",
  "detection_modules": 6
}
```

### 2. 上传文档并检测

**POST** `/api/detect`

上传Word文档并创建检测任务

**请求：**
- Content-Type: `multipart/form-data`
- 参数：
  - `file`: Word文档文件（.docx格式）

**响应示例：**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "message": "检测任务已创建，正在处理中...",
  "created_at": "2024-01-20T10:30:00"
}
```

**cURL示例：**
```bash
curl -X POST "http://localhost:8000/api/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.docx"
```

**Python示例：**
```python
import requests

url = "http://localhost:8000/api/detect"
files = {"file": open("test.docx", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(f"任务ID: {result['task_id']}")
```

### 3. 查询任务状态

**GET** `/api/status/{task_id}`

查询检测任务的状态和结果

**响应示例（处理中）：**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "created_at": "2024-01-20T10:30:00",
  "completed_at": null,
  "error": null,
  "result": null
}
```

**响应示例（已完成）：**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "created_at": "2024-01-20T10:30:00",
  "completed_at": "2024-01-20T10:30:45",
  "error": null,
  "result": {
    "total_checks": 50,
    "passed_checks": 45,
    "failed_checks": 5,
    "pass_rate": 90.0,
    "modules": {
      "Title": {...},
      "Abstract": {...},
      "Keywords": {...},
      "Content": {...},
      "Formula": {...},
      "Table": {...}
    },
    "report_url": "/api/download/123e4567-e89b-12d3-a456-426614174000/report",
    "annotated_doc_url": "/api/download/123e4567-e89b-12d3-a456-426614174000/annotated"
  }
}
```

**Python示例：**
```python
import requests
import time

task_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"http://localhost:8000/api/status/{task_id}"

# 轮询检查状态
while True:
    response = requests.get(url)
    result = response.json()
    
    if result["status"] == "completed":
        print("检测完成！")
        print(f"通过率: {result['result']['pass_rate']}%")
        break
    elif result["status"] == "failed":
        print(f"检测失败: {result['error']}")
        break
    else:
        print("检测中...")
        time.sleep(2)
```

### 4. 下载文本报告

**GET** `/api/download/{task_id}/report`

下载详细的文本格式检测报告

**响应：**
- Content-Type: `text/plain`
- 文件名：`report_{task_id}.txt`

**cURL示例：**
```bash
curl -X GET "http://localhost:8000/api/download/{task_id}/report" \
  --output report.txt
```

**Python示例：**
```python
import requests

task_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"http://localhost:8000/api/download/{task_id}/report"

response = requests.get(url)
with open("report.txt", "wb") as f:
    f.write(response.content)
```

### 5. 下载带批注的文档

**GET** `/api/download/{task_id}/annotated`

下载带有批注标记的Word文档

**响应：**
- Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- 文件名：`annotated_{task_id}.docx`

**Python示例：**
```python
import requests

task_id = "123e4567-e89b-12d3-a456-426614174000"
url = f"http://localhost:8000/api/download/{task_id}/annotated"

response = requests.get(url)
with open("annotated.docx", "wb") as f:
    f.write(response.content)
```

### 6. 删除任务

**DELETE** `/api/tasks/{task_id}`

删除任务及相关文件

**响应示例：**
```json
{
  "message": "任务已删除",
  "task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

## 完整使用流程

### Python示例

```python
import requests
import time

# 1. 上传文档
url = "http://localhost:8000/api/detect"
files = {"file": open("test.docx", "rb")}
response = requests.post(url, files=files)
task_id = response.json()["task_id"]
print(f"任务创建成功: {task_id}")

# 2. 轮询检查状态
status_url = f"http://localhost:8000/api/status/{task_id}"
while True:
    response = requests.get(status_url)
    result = response.json()
    
    if result["status"] == "completed":
        print("\n检测完成！")
        print(f"总检测项: {result['result']['total_checks']}")
        print(f"通过项: {result['result']['passed_checks']}")
        print(f"失败项: {result['result']['failed_checks']}")
        print(f"通过率: {result['result']['pass_rate']}%")
        break
    elif result["status"] == "failed":
        print(f"检测失败: {result['error']}")
        exit(1)
    else:
        print("检测中...", end="\r")
        time.sleep(2)

# 3. 下载报告
report_url = f"http://localhost:8000/api/download/{task_id}/report"
response = requests.get(report_url)
with open("report.txt", "wb") as f:
    f.write(response.content)
print("报告已下载: report.txt")

# 4. 下载带批注的文档
annotated_url = f"http://localhost:8000/api/download/{task_id}/annotated"
response = requests.get(annotated_url)
with open("annotated.docx", "wb") as f:
    f.write(response.content)
print("带批注文档已下载: annotated.docx")

# 5. （可选）删除任务
# delete_url = f"http://localhost:8000/api/tasks/{task_id}"
# requests.delete(delete_url)
```

### JavaScript示例

```javascript
// 使用fetch API
async function detectDocument(file) {
    // 1. 上传文档
    const formData = new FormData();
    formData.append('file', file);
    
    const uploadResponse = await fetch('http://localhost:8000/api/detect', {
        method: 'POST',
        body: formData
    });
    const { task_id } = await uploadResponse.json();
    console.log('任务创建成功:', task_id);
    
    // 2. 轮询检查状态
    while (true) {
        const statusResponse = await fetch(
            `http://localhost:8000/api/status/${task_id}`
        );
        const result = await statusResponse.json();
        
        if (result.status === 'completed') {
            console.log('检测完成！');
            console.log('通过率:', result.result.pass_rate, '%');
            
            // 3. 下载报告
            window.open(
                `http://localhost:8000/api/download/${task_id}/report`
            );
            
            // 4. 下载带批注的文档
            window.open(
                `http://localhost:8000/api/download/${task_id}/annotated`
            );
            
            break;
        } else if (result.status === 'failed') {
            console.error('检测失败:', result.error);
            break;
        }
        
        await new Promise(resolve => setTimeout(resolve, 2000));
    }
}
```

## 集成到系统中

### 方式1：作为微服务

将API部署到服务器上，其他系统通过HTTP请求调用：

```python
# 其他系统的集成代码
import requests

class PaperDetectionClient:
    def __init__(self, base_url="http://your-server:8000"):
        self.base_url = base_url
    
    def detect(self, file_path):
        """检测文档"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/api/detect",
                files=files
            )
            return response.json()
    
    def get_status(self, task_id):
        """获取任务状态"""
        response = requests.get(
            f"{self.base_url}/api/status/{task_id}"
        )
        return response.json()
    
    def download_report(self, task_id, output_path):
        """下载报告"""
        response = requests.get(
            f"{self.base_url}/api/download/{task_id}/report"
        )
        with open(output_path, 'wb') as f:
            f.write(response.content)

# 使用示例
client = PaperDetectionClient()
result = client.detect("test.docx")
task_id = result["task_id"]

# 等待完成后下载
status = client.get_status(task_id)
if status["status"] == "completed":
    client.download_report(task_id, "report.txt")
```

### 方式2：Docker部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

构建和运行：

```bash
docker build -t paper-detection-api .
docker run -d -p 8000:8000 paper-detection-api
```

## 配置说明

### 修改端口

在 `api.py` 最后一行修改：

```python
uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)  # 改为8080端口
```

### 配置CORS（跨域）

在 `api.py` 中修改 `allow_origins`：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://your-frontend-domain.com"],  # 指定允许的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 文件存储路径

在 `api.py` 中修改：

```python
UPLOAD_DIR = Path("/path/to/uploads")  # 上传文件目录
RESULT_DIR = Path("/path/to/results")  # 结果文件目录
```

## 注意事项

1. **文件存储**：当前版本将文件存储在本地，生产环境建议使用对象存储服务（如OSS、S3）

2. **任务持久化**：当前任务信息存储在内存中，服务重启后会丢失。生产环境建议使用数据库（如Redis、PostgreSQL）

3. **并发处理**：当前使用异步任务处理，支持并发。如需提高性能，可使用Celery等任务队列

4. **文件清理**：建议定期清理旧的上传文件和结果文件

5. **安全性**：
   - 添加身份认证（JWT、API Key等）
   - 限制文件大小
   - 添加速率限制
   - 使用HTTPS

6. **监控**：添加日志和监控，追踪API使用情况和错误

## 错误处理

API会返回标准的HTTP状态码：

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

错误响应格式：

```json
{
  "detail": "错误描述信息"
}
```

## 技术支持

如有问题，请联系开发团队或提交Issue。
