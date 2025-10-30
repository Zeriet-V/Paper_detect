# 表格检测功能总结

## 功能概述

表格检测模块 (`Table_detect.py`) 用于检测Word文档中的表格格式是否符合学术论文规范。

## 检测规则

### 1. 表格标题格式
- **格式要求**：`Table X 表名`（X为数字编号）
- **加粗**：标题必须加粗
- **对齐**：标题必须居中对齐
- **首字母大写**：表名首字母必须大写
- **字体大小**：与正文一致（小四号12pt）
- **字体**：Times New Roman

### 2. 表格编号
- 编号必须从1开始
- 编号必须连续递增（Table 1, Table 2, Table 3...）

### 3. 三线表格式
- **仅三条横线**：
  - 顶线：1.5磅
  - 表头底线：0.75磅
  - 底线：1.5磅
- **无竖线**：不应有左边框、右边框、内部竖线
- **无多余横线**：除三线外不应有其他横线

### 4. 表格内容对齐
- **表头行（第1行）**：所有单元格居中对齐
- **内容行（其他行）**：
  - 较长文本（>20字符）：左对齐
  - 较短文本（≤20字符）：居中对齐

### 5. 字体格式
- 表格内容字体应与正文保持一致
- 字体：Times New Roman
- 字号：小四号（12pt）

## 使用方法

```bash
# 基本用法
python paper_detect\Table_detect.py check <文档路径> <模板路径>

# 示例
python paper_detect\Table_detect.py check template\test.docx Table
python paper_detect\Table_detect.py check template\test.docx templates\Table.json
```

## 配置参数

在 `templates/Table.json` 中可以配置：

- `alignment_length_threshold`: 对齐判断的长度阈值（默认20字符）
- `border_width_tolerance`: 边框宽度检测容差（默认0.1磅）
- `caption_pattern`: 表格标题匹配正则表达式

## 检测报告

检测报告包含以下部分：

1. **检查总结**：整体检测结果和表格数量
2. **表格编号检查**：编号连续性验证
3. **各表格详细检查**：
   - 标题格式检查
   - 三线表格式检查（包括边框粗细）
   - 内容对齐方式检查

## 特殊处理

### 合并单元格
- 自动识别合并单元格
- 避免重复检查同一单元格
- 使用逻辑列号而非物理列号

### 对齐检测优先级
1. 直接格式（paragraph.paragraph_format.alignment）
2. 样式格式（paragraph.style.paragraph_format.alignment）
3. XML样式定义（处理样式继承）
4. 默认值（左对齐）

## 示例输出

```
============================================================
表格格式检测报告
============================================================

【检查总结】
  表格格式检查结果: 发现问题
  检测到 1 个表格

【表格编号检查】
  ✓ 表格编号正确且连续

【各表格详细检查】

  表格 1: Table 1 Material parameters
    ✓ 标题格式正确
    ✓ 三线表格式正确
    ✗ 对齐方式问题：
      - 单元格[第1行(表头),第4列]应居中对齐（当前：左对齐，内容：Density/(kg·m/s^2)）

============================================================
```

## 调试工具

使用 `debug_table_structure.py` 查看表格实际结构：

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

## 技术要点

1. **处理合并单元格**：使用单元格ID跟踪避免重复检查
2. **对齐检测**：使用 `detect_paragraph_alignment()` 函数按优先级检测
3. **边框检测**：解析XML元素获取边框宽度（以1/8磅为单位）
4. **长度阈值**：可配置的文本长度阈值用于判断对齐方式

## 依赖库

- `python-docx`: Word文档处理
- 标准库: `os`, `sys`, `json`, `re`

## 注意事项

1. Word中边框宽度以1/8磅为单位存储
2. 合并单元格会导致物理列数与逻辑列数不一致
3. 对齐方式为None时需要从样式中读取
4. 长度阈值可根据实际需求调整
