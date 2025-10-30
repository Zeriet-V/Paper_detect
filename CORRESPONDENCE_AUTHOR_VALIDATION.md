# Correspondence作者验证功能说明

## 功能概述

在之前的脚注检测增强基础上，现在进一步添加了**Correspondence作者验证**功能。系统会自动检查Correspondence字段中的作者名字是否正确，确保其与论文中的通讯作者一致。

---

## 新增功能详解

### 1. 从Correspondence中提取作者名字

**功能**：自动识别并提取Correspondence字段中的作者名字

**支持的格式**：
- 标准格式：`* Correspondence should be addressed to NAME, email: xxx`
- 简化格式：`* Correspondence: NAME, email: xxx`

**示例**：
```
输入: * Correspondence should be addressed to ZHANG Wei, email: zhang@test.com
提取: ZHANG Wei
```

---

### 2. 与论文作者列表比对

**功能**：将提取的作者名字与论文标题下的作者列表进行匹配

**匹配规则**：
- 支持完整名字匹配：`ZHANG Wei`
- 支持姓+名首字母匹配：`ZHANG W`
- 支持姓氏匹配（模糊匹配）

**示例**：
```
论文作者: ZHANG Wei*, LI Ming, WANG Hua
Correspondence: ZHANG Wei ✓ 匹配成功
Correspondence: ZHANG W   ✓ 匹配成功（名首字母）
Correspondence: LI Ming   ✓ 匹配成功
Correspondence: ZHAO Yu   ✗ 不在作者列表中
```

---

### 3. 通讯作者标记验证

**功能**：检查匹配的作者是否被标记为通讯作者

**支持的通讯作者标记**：
- `*` 星号
- `†` 剑号
- `✉` 信封符号
- 其他特殊符号

**验证逻辑**：
1. ✅ **通过**：Correspondence作者在论文作者列表中，且标记为通讯作者
2. ⚠️ **警告**：Correspondence作者在论文作者列表中，但未标记为通讯作者
3. ❌ **错误**：Correspondence作者不在论文作者列表中

---

## 检测示例

### 场景1：正确配置（通过）

**论文作者**：
```
ZHANG Wei*, LI Ming, WANG Hua
```

**脚注Correspondence**：
```
* Correspondence should be addressed to ZHANG Wei, email: zhang@dhu.edu.cn
```

**检测结果**：
```
✓ Correspondence作者'ZHANG Wei'与通讯作者'ZHANG Wei'匹配
```

---

### 场景2：作者未标记为通讯作者（警告）

**论文作者**：
```
ZHANG Wei*, LI Ming, WANG Hua
```

**脚注Correspondence**：
```
* Correspondence should be addressed to LI Ming, email: li@dhu.edu.cn
```

**检测结果**：
```
⚠️ Correspondence作者'LI Ming'在作者列表中但未标记为通讯作者（缺少*或†标记）
```

**说明**：LI Ming在作者列表中，但没有通讯作者标记，应该在作者名后添加`*`或其他标记。

---

### 场景3：作者不在列表中（错误）

**论文作者**：
```
ZHANG Wei*, LI Ming, WANG Hua
```

**脚注Correspondence**：
```
* Correspondence should be addressed to ZHAO Yu, email: zhao@test.com
```

**检测结果**：
```
❌ Correspondence作者'ZHAO Yu'不在论文作者列表中
   论文作者列表: ZHANG Wei, LI Ming, WANG Hua
```

**说明**：Correspondence中的作者名字错误或拼写有误。

---

## 技术实现

### 新增函数

#### 1. `extract_author_from_correspondence(correspondence_text)`

**功能**：从Correspondence文本中提取作者名字

**参数**：
- `correspondence_text` - Correspondence字段的完整文本

**返回**：
- `str` - 作者名字，如 `"ZHANG Wei"`
- `None` - 无法提取

**实现位置**：`Keywords_detect.py` 第989-1005行

---

#### 2. `match_author_name(correspondence_name, paper_authors)`

**功能**：匹配Correspondence中的作者与论文作者列表

**参数**：
- `correspondence_name` - 从Correspondence提取的作者名字
- `paper_authors` - 论文作者列表（字典数组）

**返回**：
- `(matched_author, is_corresponding)` - 元组
  - `matched_author` - 匹配的作者字典，包含姓、名、通讯作者标记等信息
  - `is_corresponding` - 布尔值，表示是否为通讯作者

**实现位置**：`Keywords_detect.py` 第1007-1037行

---

### 集成位置

在 `check_footnote_structure()` 函数中，Correspondence检查部分（第1173-1227行）：

```python
# 检查Correspondence（正确拼写）
if re.search(correspondence_pattern, footnote_text, re.IGNORECASE):
    found_items['correspondence'] = True
    
    # 新增：检查Correspondence中的作者是否正确
    if TITLE_DETECT_AVAILABLE:
        # 1. 提取Correspondence中的作者名字
        corr_author_name = extract_author_from_correspondence(footnote_text)
        
        # 2. 提取论文作者信息
        doc_info = extract_paper_title_authors(doc, tpl)
        
        # 3. 匹配作者
        matched_author, is_corresponding = match_author_name(
            corr_author_name, 
            doc_info['authors']
        )
        
        # 4. 验证结果并报告
        if matched_author and is_corresponding:
            # 通过
        elif matched_author and not is_corresponding:
            # 警告：未标记为通讯作者
        else:
            # 错误：不在作者列表中
```

---

## 配置选项

在 `templates/Keywords.json` 中新增的消息：

```json
{
  "messages": {
    "footnote_correspondence_author_not_found": "Correspondence中的作者不在论文作者列表中",
    "footnote_correspondence_author_not_corresponding": "Correspondence中的作者未标记为通讯作者",
    "footnote_correspondence_author_match": "Correspondence中的作者与论文通讯作者匹配"
  }
}
```

---

## 使用方法

### 命令行运行

```bash
python paper_detect\Keywords_detect.py check paper.docx templates\Keywords.json
```

### 运行测试

```bash
python test_correspondence_author.py
```

---

## 完整检测流程

脚注Correspondence字段的完整检测流程如下：

```
1. 检查Correspondence拼写
   ├─ ✓ 正确：Correspondence
   └─ ✗ 错误：Corresponding

2. 提取Correspondence中的作者名字
   ├─ ✓ 提取成功
   └─ ⚠️ 无法提取

3. 与论文作者列表比对
   ├─ ✓ 找到匹配作者
   └─ ✗ 未找到匹配作者

4. 检查是否为通讯作者
   ├─ ✓ 是通讯作者（有*、†、✉等标记）
   └─ ⚠️ 不是通讯作者（缺少标记）
```

---

## 示例报告

### 成功报告

```
--- FOOTNOTE STRUCTURE ---
 OK: True
  - Received date格式正确
  - Foundation item格式正确
  - ✓ Correspondence作者'ZHANG Wei'与通讯作者'ZHANG Wei'匹配
  - Correspondence格式正确
  - Citation格式正确
  - ✓ Citation标题与论文标题一致（sentence case格式）
  - 脚注结构检测通过
```

### 警告报告

```
--- FOOTNOTE STRUCTURE ---
 OK: False
  - Received date格式正确
  - Foundation item格式正确
  - ⚠️ Correspondence作者'LI Ming'在作者列表中但未标记为通讯作者（缺少*或†标记）
  - Citation格式正确
```

### 错误报告

```
--- FOOTNOTE STRUCTURE ---
 OK: False
  - Received date格式正确
  - Foundation item格式正确
  - ❌ Correspondence作者'ZHAO Yu'不在论文作者列表中
     论文作者列表: ZHANG Wei, LI Ming, WANG Hua
  - Citation格式正确
```

---

## 注意事项

### 1. 模块依赖

- 需要 `Title_detect.py` 模块来提取论文作者
- 如果该模块不可用，Correspondence作者验证将被跳过
- 基本的Correspondence格式检查仍会执行

### 2. 作者名字格式

**论文中的作者格式**：
```
SURNAME Givenname
```

**Correspondence中的作者格式**（支持两种）：
- 完整名字：`SURNAME Givenname`
- 姓+名首字母：`SURNAME G`

### 3. 通讯作者标记

论文作者列表中的通讯作者必须有明确标记：
```
ZHANG Wei*        ✓ 星号标记
ZHANG Wei†        ✓ 剑号标记
ZHANG Wei✉        ✓ 信封标记
ZHANG Wei         ✗ 无标记
```

### 4. 多个通讯作者

如果有多个通讯作者：
```
ZHANG Wei*, LI Ming†, WANG Hua
```

Correspondence可以指向任意一个标记了的通讯作者。

---

## 测试验证

### 测试脚本

运行 `test_correspondence_author.py` 验证功能：

```bash
python test_correspondence_author.py
```

### 测试覆盖

✅ 从Correspondence提取作者名字  
✅ 完整名字匹配  
✅ 姓+名首字母匹配  
✅ 通讯作者标记识别  
✅ 作者不在列表中的检测  
✅ 作者未标记为通讯作者的检测  

---

## 总结

### 完整的Correspondence检测功能

1. ✅ **拼写检查**：Correspondence vs Corresponding
2. ✅ **格式检查**：标准格式验证
3. ✅ **作者提取**：自动提取作者名字
4. ✅ **作者匹配**：与论文作者列表比对
5. ✅ **通讯作者验证**：检查是否标记为通讯作者

### 三级验证结果

- ✅ **通过**：Correspondence作者正确且为通讯作者
- ⚠️ **警告**：Correspondence作者存在但未标记
- ❌ **错误**：Correspondence作者不在列表中

这确保了脚注中的Correspondence信息与论文主体内容完全一致，提高了论文格式的准确性和一致性。
