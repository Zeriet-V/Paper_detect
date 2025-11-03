# 脚注字段拼写错误检测

## 功能说明

在脚注检测中，新增了**字段拼写错误自动识别**功能。系统会检测常见的拼写错误并给出明确的纠正提示。

---

## 常见拼写错误

### 1. Received date

| 正确 ✅ | 常见错误 ❌ | 说明 |
|---------|------------|------|
| `Received date:` | `Receive date:` | 缺少'd' |

**检测示例**：
```
脚注内容: Receive date: 2023-10-06
检测结果: ❌ Received date拼写错误：应为'Received date'而不是'Receive date'（缺少'd'）
```

---

### 2. Foundation item

| 正确 ✅ | 常见错误 ❌ | 说明 |
|---------|------------|------|
| `Foundation item:` | `Foundation items:` | 多了's'，应该用单数 |

**检测示例**：
```
脚注内容: Foundation items: National Natural Science Foundation
检测结果: ❌ Foundation item拼写错误：应为'Foundation item'而不是'Foundation items'（单数形式）
```

---

### 3. Correspondence

| 正确 ✅ | 常见错误 ❌ | 说明 |
|---------|------------|------|
| `Correspondence` | `Corresponding` | 错用了形容词形式 |

**检测示例**：
```
脚注内容: * Corresponding should be addressed to...
检测结果: ❌ Correspondence拼写错误：应为'Correspondence'而不是'Corresponding'
```

---

## 检测逻辑

### 1. 优先匹配正确格式
系统首先尝试匹配正确的拼写格式：
```python
if re.search(r'Received date\s*:', text):
    # 格式正确
```

### 2. 检测常见错误
如果正确格式未匹配，检查常见的拼写错误：
```python
elif re.search(r'Receive date\s*:', text):
    # 发现拼写错误
    报告错误并给出纠正建议
```

### 3. 报告缺失
如果两者都未匹配，报告字段缺失：
```python
else:
    # 字段缺失
    报告"未找到xxx项目"
```

---

## 使用示例

### 测试文档

假设脚注内容如下：
```
Receive date: 2023-10-06
Foundation items: National Natural Science Foundation (No. 51705545)
* Corresponding should be addressed to ZHANG Wei, email: zhang@dhu.edu.cn
Citation: ...
```

### 检测结果

```
--- FOOTNOTE STRUCTURE ---
 OK: False
  - ❌ Received date拼写错误：应为'Received date'而不是'Receive date'（缺少'd'）
  - ❌ Foundation item拼写错误：应为'Foundation item'而不是'Foundation items'（单数形式）
  - ❌ Correspondence拼写错误：应为'Correspondence'而不是'Corresponding'
  - Citation格式正确
```

### 修正后

```
Received date: 2023-10-06
Foundation item: National Natural Science Foundation (No. 51705545)
* Correspondence should be addressed to ZHANG Wei, email: zhang@dhu.edu.cn
Citation: ...
```

### 检测结果（修正后）

```
--- FOOTNOTE STRUCTURE ---
 OK: True
  - Received date格式正确
  - Foundation item格式正确
  - Correspondence格式正确
  - Citation格式正确
  - 脚注结构检测通过
```

---

## 实现细节

### 代码位置

`paper_detect/Keywords_detect.py` 中的 `check_footnote_structure()` 函数

### Received date检测
```python
# 检查Received date（正确拼写）
if re.search(received_pattern, footnote_text, re.IGNORECASE):
    found_items['received'] = True
    report['messages'].append("Received date格式正确")
# 检查常见错误：Receive date（少了d）
elif re.search(r'Receive\s+date\s*:', footnote_text, re.IGNORECASE):
    found_items['received'] = False
    report['ok'] = False
    report['messages'].append("❌ Received date拼写错误：应为'Received date'而不是'Receive date'（缺少'd'）")
```

### Foundation item检测
```python
# 检查Foundation item（正确拼写）
if re.search(foundation_pattern, footnote_text, re.IGNORECASE):
    found_items['foundation'] = True
    report['messages'].append("Foundation item格式正确")
# 检查常见错误：Foundation items（多了s）
elif re.search(r'Foundation\s+items\s*:', footnote_text, re.IGNORECASE):
    found_items['foundation'] = False
    report['ok'] = False
    report['messages'].append("❌ Foundation item拼写错误：应为'Foundation item'而不是'Foundation items'（单数形式）")
```

### Correspondence检测
```python
# 检查Correspondence（正确拼写）
if re.search(correspondence_pattern, footnote_text, re.IGNORECASE):
    found_items['correspondence'] = True
    # ... 进行作者验证
# 检查常见错误：Corresponding
elif re.search(r'\*\s*Corresponding\s+', footnote_text, re.IGNORECASE):
    found_items['correspondence'] = False
    report['ok'] = False
    report['messages'].append("❌ Correspondence拼写错误：应为'Correspondence'而不是'Corresponding'")
```

---

## 配置文件

在 `templates/Keywords.json` 中添加了相应的错误消息：

```json
{
  "messages": {
    "footnote_received_spelling_error": "Received date拼写错误，应为'Received date'而不是'Receive date'",
    "footnote_foundation_spelling_error": "Foundation item拼写错误，应为'Foundation item'（单数）而不是'Foundation items'（复数）",
    "footnote_correspondence_spelling_error": "Correspondence拼写错误，应为'Correspondence'而不是'Corresponding'"
  }
}
```

---

## 检测优先级

检测按以下优先级进行：

1. **正确格式匹配** → ✅ 通过
2. **拼写错误检测** → ❌ 明确错误提示
3. **字段缺失** → ⚠️ 未找到项目

这样可以为用户提供更精确的错误定位和修改建议。

---

## 测试验证

### 命令行测试

```bash
python paper_detect\Keywords_detect.py check template\test.docx templates\Keywords.json
```

### 预期输出

如果文档中有拼写错误：
```
--- FOOTNOTE STRUCTURE ---
 OK: False
  - ❌ Received date拼写错误：应为'Received date'而不是'Receive date'（缺少'd'）
  - Foundation item格式正确
  - Correspondence格式正确
  - Citation格式正确
```

---

## 总结

### 新增的拼写检测

✅ **Received date** - 检测缺少'd'的错误  
✅ **Foundation item** - 检测多余's'的错误  
✅ **Correspondence** - 检测错用Corresponding的错误  

### 检测特点

- 🎯 **精确定位**：明确指出具体的拼写错误
- 📝 **清晰建议**：给出正确的拼写格式
- 🔍 **智能识别**：区分拼写错误和字段缺失

### 用户体验改进

之前：
```
❌ 脚注中未找到received项目  （用户不知道是拼写错误还是真的缺失）
```

现在：
```
❌ Received date拼写错误：应为'Received date'而不是'Receive date'（缺少'd'）
```

这大大提高了错误提示的可用性，用户可以快速定位和修正问题。

---

## 版本信息

- **功能版本**: 2.2
- **更新日期**: 2025-10-24
- **新增功能**: 脚注字段拼写错误自动检测
