# 脚注检测功能增强说明

## 概述

本次更新为Keywords_detect.py中的脚注检测功能添加了多项智能检测能力，确保脚注内容与论文主体内容的一致性。

## 新增功能

### 1. Correspondence拼写错误检测

**功能说明：**
- 自动检测Correspondence字段是否错误拼写为"Corresponding"
- 这是一个常见的拼写错误，系统现在可以明确指出

**检测规则：**
- ✅ 正确：`* Correspondence should be addressed to NAME, email: xxx`
- ❌ 错误：`* Corresponding should be addressed to NAME, email: xxx`

**错误提示示例：**
```
❌ Correspondence拼写错误：应为'Correspondence'而不是'Corresponding'
```

---

### 2. 作者信息比对

**功能说明：**
- 自动提取论文标题下的作者列表
- 将Citation中的作者与论文作者进行比对
- 检查作者数量、顺序和姓名是否一致

**检测规则：**
- Citation中必须包含前三位作者
- 作者顺序必须与论文中的顺序一致
- 作者姓名缩写必须正确匹配

**比对示例：**

论文作者：
```
ZHANG Wei, LI Ming, WANG Xiaohong
```

Citation期望格式：
```
ZHANG W, LI M, WANG X, et al. Title [J]. Journal...
```

**错误提示示例：**
```
❌ Citation中作者数量(2个)与论文作者数量(3个)不匹配
❌ Citation中第2位作者'LI H'与论文作者'LI MING'不匹配
```

---

### 3. 标题内容比对

**功能说明：**
- 自动提取论文标题
- 将Citation中的标题与论文标题进行比对
- 自动处理Title Case到Sentence Case的转换

**检测规则：**
- Citation中的标题必须与论文标题内容一致
- Citation使用Sentence Case格式（仅首字母大写）
- 论文标题通常使用Title Case格式（每个实词首字母大写）
- 系统会自动进行格式转换后比对

**格式转换示例：**

论文标题（Title Case）：
```
Study on the Effect of Temperature on Polymer Synthesis
```

Citation期望标题（Sentence Case）：
```
Study on the effect of temperature on polymer synthesis
```

**特殊处理：**
- 专有名词（如FePc, SQL）保留原有大小写
- 化学式保留原有格式

**错误提示示例：**
```
❌ Citation中的标题与论文标题不一致
   论文标题: Study on the Effect of Temperature on Polymer Synthesis
   期望格式(sentence case): Study on the effect of temperature on polymer synthesis
   实际Citation: Study on the temperature effect for polymer synthesis
```

**成功提示示例：**
```
✓ Citation标题与论文标题一致（sentence case格式）
```

---

## 技术实现

### 依赖模块
- 导入`Title_detect`模块用于提取论文作者和标题
- 如果无法导入，相关比对功能将被禁用，但基本检测仍可正常工作

### 核心函数

1. **`title_to_sentence_case(title)`**
   - 将Title Case转换为Sentence Case
   - 保留专有名词和化学式的大小写

2. **`normalize_author_name(author_str)`**
   - 标准化作者姓名格式用于比对
   - 移除多余空格和标点

3. **`extract_authors_from_citation(citation_text)`**
   - 从Citation文本中提取作者列表

4. **`extract_title_from_citation(citation_text)`**
   - 从Citation文本中提取标题

5. **`extract_paper_title_authors(doc, tpl)`**
   - 从论文文档中提取标题和作者信息
   - 返回结构化的作者和标题数据

### 配置文件更新

在`templates/Keywords.json`中新增：

```json
{
  "author_regex": "^([A-Z]+)\\s+([A-Z\\s]+)$",
  "structure_rules": {
    "footnote_corresponding_wrong_pattern": "\\*\\s*Corresponding\\s+",
    "enable_author_title_comparison": true
  },
  "messages": {
    "footnote_correspondence_spelling_error": "Correspondence拼写错误，应为'Correspondence'而不是'Corresponding'",
    "footnote_author_mismatch": "Citation中的作者与论文作者不匹配",
    "footnote_title_mismatch": "Citation中的标题与论文标题不匹配",
    "footnote_title_case_error": "Citation中标题应使用sentence case格式（仅首字母大写）"
  }
}
```

---

## 使用方法

### 命令行使用

```bash
python paper_detect\Keywords_detect.py check <paper.docx> templates\Keywords.json
```

### 检测报告示例

```
=== Paper Format Check Report ===
--- FOOTNOTE STRUCTURE ---
 OK: True
  - Received date格式正确
  - Foundation item格式正确
  - Correspondence格式正确
  - Citation格式正确
  - ✓ Citation标题与论文标题一致（sentence case格式）
  - 脚注结构检测通过
```

### 错误报告示例

```
=== Paper Format Check Report ===
--- FOOTNOTE STRUCTURE ---
 OK: False
  - Received date格式正确
  - Foundation item格式正确
  - ❌ Correspondence拼写错误：应为'Correspondence'而不是'Corresponding'
  - Citation格式正确
  - ❌ Citation中第1位作者'ZHANG H'与论文作者'ZHANG WEI'不匹配
  - ❌ Citation中的标题与论文标题不一致
     论文标题: Study on the Effect of Temperature
     期望格式(sentence case): Study on the effect of temperature
     实际Citation: Research on temperature effects
```

---

## 注意事项

1. **模块依赖**：确保`Title_detect.py`在同一目录下，否则作者/标题比对功能将被禁用

2. **作者格式**：论文作者应使用标准格式：`SURNAME Givenname`（姓全大写，名首字母大写）

3. **Citation格式**：Citation中作者应为缩写格式：`SURNAME I` 或 `SURNAME I N`

4. **标题大小写**：
   - 论文标题使用Title Case（每个实词首字母大写）
   - Citation标题使用Sentence Case（仅首字母大写）
   - 系统会自动进行转换比对

5. **特殊词汇**：化学式、缩写词等特殊大小写会被保留

---

## 测试建议

### 测试用例1：Correspondence拼写错误
```
脚注内容：* Corresponding should be addressed to...
期望结果：检测出拼写错误
```

### 测试用例2：作者顺序错误
```
论文作者：ZHANG Wei, LI Ming, WANG Hua
Citation：LI M, ZHANG W, WANG H, et al. Title...
期望结果：检测出作者顺序不一致
```

### 测试用例3：标题格式错误
```
论文标题：Study on the Effect of Temperature
Citation标题：Study On The Effect Of Temperature (使用了Title Case而非Sentence Case)
期望结果：检测出标题大小写格式错误
```

---

## 未来改进方向

1. 支持更灵活的作者姓名匹配（考虑多种缩写形式）
2. 增加对中文名的处理
3. 支持更多Journal名称的检测
4. 提供更详细的修改建议

---

## 版本信息

- **版本**: 2.0
- **更新日期**: 2025-10-24
- **更新内容**: 增强脚注检测功能，添加作者和标题比对
