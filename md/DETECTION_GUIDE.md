# 学术论文格式检测系统 - 完整指南

## 📋 目录

- [系统概述](#系统概述)
- [检测模块](#检测模块)
  - [1. 摘要检测 (Abstract)](#1-摘要检测-abstract)
  - [2. 标题检测 (Title)](#2-标题检测-title)
  - [3. 公式检测 (Formula)](#3-公式检测-formula)
  - [4. 表格检测 (Table)](#4-表格检测-table)
- [使用方法](#使用方法)
- [配置说明](#配置说明)
- [调试工具](#调试工具)

---

## 系统概述

本系统用于自动检测Word文档(.docx)中的学术论文格式是否符合规范，包括摘要、标题、公式、表格等元素的格式检查。

### 核心特性

- ✅ 全面的格式检查（字体、字号、对齐、间距等）
- ✅ 详细的错误报告
- ✅ 可配置的检测规则（JSON模板）
- ✅ 支持中英文混排
- ✅ 处理复杂格式（合并单元格、样式继承等）

### 技术栈

- Python 3.x
- python-docx
- JSON配置

---

## 检测模块

### 1. 摘要检测 (Abstract)

#### 检测内容

**结构检查**
- 摘要必须以"Abstract:"开头
- 摘要长度应在合理范围内（可配置，默认100-500字）
- 摘要不应过短或过长

**段落检查**
- 摘要内容应为单一段落
- 不应包含多个段落

**格式检查**
- **字体**：Times New Roman
- **字号**：小四号（12pt）
- **加粗**：是
- **斜体**：否
- **行间距**：1.5倍行距
- **对齐方式**：两端对齐
- **缩进**：首行缩进0pt，左右缩进0pt

#### 使用方法

```bash
# 基本用法
python paper_detect\Abstract_detect.py check <文档路径> <模板路径>

# 示例
python paper_detect\Abstract_detect.py check template\test.docx Abstract
python paper_detect\Abstract_detect.py check template\test.docx templates\Abstract.json
```

#### 配置文件

`templates/Abstract.json`

```json
{
  "format_rules": {
    "font_size_pt": 12,
    "font_name": "Times New Roman",
    "bold": true,
    "italic": false,
    "line_spacing": 1.5,
    "alignment": "justify",
    "first_line_indent": 0,
    "left_indent": 0,
    "right_indent": 0
  },
  "check_rules": {
    "min_length": 100,
    "max_length": 500
  }
}
```

---

### 2. 标题检测 (Title)

#### 检测内容

**标题格式**
- **字体**：Times New Roman
- **字号**：小二号（18pt）
- **加粗**：是
- **对齐**：居中

**作者格式**
- **字体**：Times New Roman
- **字号**：小四号（12pt）
- **加粗**：否
- **对齐**：居中

**单位/地址格式**
- **字体**：Times New Roman
- **字号**：小四号（12pt）
- **加粗**：否
- **对齐**：居中

#### 使用方法

```bash
python paper_detect\Title_detect.py check <文档路径> <模板路径>
```

#### 特殊处理

- 支持多个作者
- 支持多个单位/地址
- 自动识别作者和单位的分隔符

---

### 3. 公式检测 (Formula)

#### 检测内容

**公式格式**
- **制表位设置**：
  - 第一个制表位：20字符（居中对齐）- 用于公式居中
  - 第二个制表位：40字符（右对齐）- 用于编号右对齐
- **Office Math对象**：必须包含Word的数学对象
- **字体**：Cambria Math（数学公式默认字体）

**公式编号**
- 编号必须从(1)开始
- 编号必须连续递增 (1), (2), (3)...
- 编号格式：`(数字)`

**公式位置**
- 公式居中显示
- 编号右对齐

#### 使用方法

```bash
python paper_detect\Formula_detect.py check <文档路径> <模板路径>
```

#### 配置文件

`templates/Formula.json`

```json
{
  "format_rules": {
    "tab_stops": {
      "center": 20,
      "right": 40
    },
    "require_math_object": true,
    "font_name": "Cambria Math"
  },
  "check_rules": {
    "numbering_check": true,
    "numbering_start": 1
  }
}
```

#### 检测示例

```
正确格式：
    公式内容居中                                    (1)
    
检测项目：
✓ 制表位设置正确（20字符居中，40字符右对齐）
✓ 包含Office Math对象
✓ 公式编号从(1)开始且连续
```

---

### 4. 表格检测 (Table)

#### 检测内容

**表格标题**
- **格式**：`Table X 表名`（X为数字编号）
- **字体**：Times New Roman
- **字号**：五号（10.5pt）
- **加粗**：是
- **对齐**：居中
- **首字母大写**：表名首字母必须大写

**表格编号**
- 编号必须从1开始
- 编号必须连续递增（Table 1, Table 2, Table 3...）

**三线表格式**
- **仅三条横线**：
  - **顶线**：1.5磅（表格第一行的顶边框）
  - **表头底线**：0.75磅（第一行的底边框）
  - **底线**：1.5磅（最后一行的底边框）
- **无竖线**：不应有左边框、右边框、内部竖线
- **无多余横线**：除三线外不应有其他横线

**表格内容对齐**
- **表头行（第1行）**：所有单元格居中对齐
- **内容行（其他行）**：
  - 较长文本（>20字符）：左对齐
  - 较短文本（≤20字符）：居中对齐

**表格内容字体**
- **字体**：Times New Roman
- **字号**：五号（10.5pt）

#### 使用方法

```bash
python paper_detect\Table_detect.py check <文档路径> <模板路径>
```

#### 配置文件

`templates/Table.json`

```json
{
  "table_detection_rules": {
    "caption_pattern": "^\\s*Table\\s+(\\d+)\\s+(.+)$",
    "table_style": {
      "type": "three_line",
      "border_width": {
        "top_line": 1.5,
        "bottom_line": 1.5,
        "header_line": 0.75,
        "unit": "pt"
      }
    },
    "content_alignment": {
      "header_row": "center",
      "content_long": "left",
      "content_short": "center"
    }
  },
  "format_rules": {
    "caption": {
      "font_size_pt": 10.5,
      "font_name": "Times New Roman",
      "bold": true,
      "alignment": "center"
    },
    "table_content": {
      "font_size_pt": 10.5,
      "font_name": "Times New Roman"
    }
  },
  "check_rules": {
    "alignment_length_threshold": 20,
    "border_width_tolerance": 0.1,
    "border_width_check": true
  }
}
```

#### 特殊处理

**合并单元格**
- 自动识别合并单元格
- 避免重复检查同一单元格
- 使用逻辑列号而非物理列号

**边框检测**
- 三线表的边框通常设置在单元格级别
- 检查第一行的顶边框（顶线）
- 检查第一行的底边框（表头底线）
- 检查最后一行的底边框（底线）

#### 检测报告示例

```
============================================================
表格格式检测报告
============================================================

【检查总结】
  表格格式检查结果: 通过
  检测到 1 个表格

【表格编号检查】
  ✓ 表格编号正确且连续

【各表格详细检查】

  表格 1: Table 1 Material parameters
    ✓ 标题格式正确
    ✓ 三线表格式正确
    ✓ 内容对齐方式正确

============================================================
```

---

## 使用方法

### 通用命令格式

```bash
python paper_detect\<模块名>_detect.py check <文档路径> <模板路径>
```

### 快速开始

1. **准备文档**：将待检测的Word文档放在项目目录下

2. **运行检测**：
   ```bash
   # 检测摘要
   python paper_detect\Abstract_detect.py check your_doc.docx Abstract
   
   # 检测标题
   python paper_detect\Title_detect.py check your_doc.docx Title
   
   # 检测公式
   python paper_detect\Formula_detect.py check your_doc.docx Formula
   
   # 检测表格
   python paper_detect\Table_detect.py check your_doc.docx Table
   ```

3. **查看报告**：检测结果会直接显示在终端

### 批量检测

创建批处理脚本：

```batch
@echo off
echo 开始全面检测...

echo.
echo ========== 检测摘要 ==========
python paper_detect\Abstract_detect.py check template\test.docx Abstract

echo.
echo ========== 检测标题 ==========
python paper_detect\Title_detect.py check template\test.docx Title

echo.
echo ========== 检测公式 ==========
python paper_detect\Formula_detect.py check template\test.docx Formula

echo.
echo ========== 检测表格 ==========
python paper_detect\Table_detect.py check template\test.docx Table

echo.
echo 检测完成！
pause
```

---

## 配置说明

### JSON模板结构

所有模板文件都遵循相似的JSON结构：

```json
{
  "format_rules": {
    // 格式要求
    "font_size_pt": 12,
    "font_name": "Times New Roman",
    "bold": false,
    "italic": false,
    "alignment": "center",
    "line_spacing": 1.5
  },
  "check_rules": {
    // 检查规则
    "min_length": 100,
    "max_length": 500
  },
  "messages": {
    // 错误消息模板
    "error_key": "错误描述"
  },
  "notes": [
    // 说明文档
  ]
}
```

### 常用配置项

#### 字体设置
- `font_size_pt`: 字号（磅值）
- `font_name`: 字体名称
- `bold`: 是否加粗
- `italic`: 是否斜体

#### 对齐方式
- `"left"`: 左对齐
- `"center"`: 居中
- `"right"`: 右对齐
- `"justify"`: 两端对齐

#### 间距设置
- `line_spacing`: 行间距（倍数）
- `space_before`: 段前间距（磅）
- `space_after`: 段后间距（磅）

#### 缩进设置
- `first_line_indent`: 首行缩进（磅）
- `left_indent`: 左缩进（磅）
- `right_indent`: 右缩进（磅）

### 字号对照表

在 `check_rules.font_size_mapping` 中定义：

```json
{
  "9": "小五",
  "10.5": "五号",
  "12": "小四",
  "14": "四号",
  "15": "小三",
  "16": "三号",
  "18": "小二",
  "22": "二号",
  "24": "小一",
  "26": "一号"
}
```

---

## 调试工具

### 1. 表格结构查看器

查看表格的实际结构（行数、列数、合并单元格）：

```bash
python debug_table_structure.py template\test.docx
```

输出示例：
```
文档中共有 1 个表格

表格 1
行数: 3
列数: 6

第 1 行 - 包含 6 个单元格:
  列 1: Material parameter
  列 2: Material
  列 3 [合并]: Material
  列 4: Poisson's ratio
  列 5 [合并]: Poisson's ratio
  列 6: Density/(kg·m/s^2)
```

### 2. 边框宽度查看器

查看表格边框的实际宽度：

```bash
python debug_border_width.py template\test.docx
```

输出示例：
```
【各行单元格边框】

  第 1 行:
    顶线: 12 (= 1.50磅), 类型: single
    底线: 6 (= 0.75磅), 类型: single

  第 2 行:
    顶线: 无
    底线: 无

  第 3 行:
    顶线: 无
    底线: 12 (= 1.50磅), 类型: single
```

**说明**：Word中边框宽度以1/8磅为单位存储
- 12 = 1.5磅
- 6 = 0.75磅
- 8 = 1磅

---

## 技术要点

### 对齐检测优先级

检测对齐方式时按以下优先级：

1. **直接格式**：`paragraph.paragraph_format.alignment`
2. **样式格式**：`paragraph.style.paragraph_format.alignment`
3. **XML样式**：从styles.xml中读取样式定义
4. **默认值**：左对齐（0）

这种分层检测可以正确处理样式继承的情况。

### 字体检测

字体检测会考虑：
- Run级别的字体设置
- 段落样式的字体设置
- 中英文字体分别设置的情况

### 数学公式检测

公式检测通过以下方式识别：
1. 检查段落是否包含Office Math对象
2. 检查制表位设置（居中+右对齐）
3. 检查段落样式是否为公式样式
4. 检查是否包含公式编号模式

### 合并单元格处理

表格检测中通过单元格ID跟踪避免重复检查：

```python
checked_cells = set()
for cell in row.cells:
    cell_id = id(cell._element)
    if cell_id in checked_cells:
        continue  # 跳过合并的重复单元格
    checked_cells.add(cell_id)
```

---

## 常见问题

### Q: 为什么对齐方式检测不准确？

A: Word文档中对齐方式可能通过样式设置，如果直接格式为None，需要从样式中读取。使用 `detect_paragraph_alignment()` 函数可以正确处理这种情况。

### Q: 表格列数显示不正确？

A: 这通常是由于合并单元格导致的。物理列数包含合并的重复单元格，而逻辑列数是实际的列数。使用调试工具可以查看表格真实结构。

### Q: 边框宽度检测为什么检测不到？

A: 三线表的边框通常设置在单元格级别而非表格级别。需要检查第一行和最后一行单元格的边框，而不是表格的全局边框设置。

### Q: 如何调整检测容差？

A: 在JSON模板的 `check_rules` 中设置：
- `border_width_tolerance`: 边框宽度容差（默认0.1磅）
- `alignment_length_threshold`: 对齐判断的长度阈值（默认20字符）

---

## 扩展开发

### 添加新的检测模块

1. 创建新的检测脚本：`NewModule_detect.py`
2. 创建对应的JSON模板：`templates/NewModule.json`
3. 实现核心检测函数
4. 添加命令行接口
5. 更新本文档

### 模板结构建议

```python
def check_new_module(doc, tpl):
    """
    检测新模块
    返回：检测结果字典
    """
    report = {
        'ok': True,
        'messages': []
    }
    
    # 实现检测逻辑
    
    return report
```

---

## 版本信息

- **当前版本**：1.0
- **Python版本要求**：3.6+
- **依赖库**：python-docx

## 更新日志

### v1.0 (2024)
- ✅ 实现摘要格式检测
- ✅ 实现标题格式检测
- ✅ 实现公式格式检测
- ✅ 实现表格格式检测（三线表）
- ✅ 支持合并单元格处理
- ✅ 支持边框粗细检测
- ✅ 添加调试工具
- ✅ 完善对齐方式检测（样式继承）

---

## 联系与支持

如有问题或建议，请联系开发团队。

---

**文档更新日期**：2024年10月
