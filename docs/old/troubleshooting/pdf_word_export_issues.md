# PDF/Word 导出问题排查指南

## 问题 1: 中文文本竖排显示

### 问题描述

在将 Markdown 报告导出为 PDF 或 Word 文档时，部分中文文本被错误地显示为竖排（从上到下），而不是正常的横排（从左到右）。

### 问题示例

```bash
报
告
生
成
时
间
：
2
0
2
5
年
1
1
月
0
5
日

```bash

### 根本原因

1. **Pandoc 默认行为**：Pandoc 在处理某些中文内容时，可能会自动应用竖排文本样式（`writing-mode: vertical-rl`）
2. **缺少语言和方向指定**：没有明确告诉 Pandoc 文档的语言和文本方向
3. **HTML/CSS 样式干扰**：Markdown 内容中可能包含了错误的 HTML 标签或 CSS 样式

### 解决方案

#### 1. 明确指定文本方向（已实现）

在 `app/utils/report_exporter.py` 中，为 Pandoc 添加了以下参数：

- *Word 文档**：

```python
extra_args = [
    '--from=markdown-yaml_metadata_block',
    '--standalone',
    '--wrap=preserve',
    '--columns=120',
    '-M', 'lang=zh-CN',  # 🔥 明确指定语言为简体中文
    '-M', 'dir=ltr',     # 🔥 明确指定文本方向为从左到右

]

```bash

- *PDF 文档**：

```python
extra_args = [
    '--from=markdown-yaml_metadata_block',
    '-V', 'mainfont=Noto Sans CJK SC',
    '-V', 'sansfont=Noto Sans CJK SC',
    '-V', 'monofont=Noto Sans Mono CJK SC',
    '--wrap=preserve',
    '--columns=120',
    '-V', 'geometry:margin=2cm',
    '-M', 'lang=zh-CN',  # 🔥 明确指定语言为简体中文
    '-M', 'dir=ltr',     # 🔥 明确指定文本方向为从左到右
    f'--css={css_file_path}',
]

```bash

#### 2. 添加 CSS 样式强制横排（已实现）

在 `_create_pdf_css()` 方法中，添加了强制横排的 CSS 样式：

```css
/*🔥 强制所有文本横排显示（修复中文竖排问题）*/

- {

    writing-mode: horizontal-tb !important;
    text-orientation: mixed !important;
}

body {
    writing-mode: horizontal-tb !important;
    direction: ltr !important;
}

p, div, span, td, th, li {
    writing-mode: horizontal-tb !important;
    text-orientation: mixed !important;
}

```bash

#### 3. 清理 Markdown 内容（已实现）

在 `_clean_markdown_for_pandoc()` 方法中，添加了以下清理逻辑：

```python

# 移除可能导致竖排的 HTML 标签和样式

md_content = re.sub(r'<[^>]*writing-mode[^>]*>', '', md_content, flags=re.IGNORECASE)
md_content = re.sub(r'<[^>]*text-orientation[^>]*>', '', md_content, flags=re.IGNORECASE)

# 移除 <div> 标签中的 style 属性

md_content = re.sub(r'<div\s+style="[^"]*">', '<div>', md_content, flags=re.IGNORECASE)
md_content = re.sub(r'<span\s+style="[^"]*">', '<span>', md_content, flags=re.IGNORECASE)

# 移除 <style> 标签

md_content = re.sub(r'<style[^>]*>.*?</style>', '', md_content, flags=re.DOTALL | re.IGNORECASE)

```bash

#### 4. Word 文档后处理（已实现）

使用 `python-docx` 库对生成的 Word 文档进行后处理，移除错误的文本方向设置：

```python
from docx import Document
doc = Document(output_file)

# 修复所有段落的文本方向

for paragraph in doc.paragraphs:
    if paragraph._element.pPr is not None:
        for child in list(paragraph._element.pPr):
            if 'textDirection' in child.tag or 'bidi' in child.tag:
                paragraph._element.pPr.remove(child)

# 修复表格中的文本方向

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                if paragraph._element.pPr is not None:
                    for child in list(paragraph._element.pPr):
                        if 'textDirection' in child.tag or 'bidi' in child.tag:
                            paragraph._element.pPr.remove(child)

doc.save(output_file)

```bash

### 测试方法

1. **生成测试报告**：

   ```bash

# 在前端或 API 中生成一份包含中文内容的分析报告
   ```

1. **导出为 Word**：
   - 点击"导出为 Word"按钮
   - 打开生成的 `.docx` 文件
   - 检查所有中文文本是否都是横排显示

1. **导出为 PDF**：
   - 点击"导出为 PDF"按钮
   - 打开生成的 `.pdf` 文件
   - 检查所有中文文本是否都是横排显示

### 如果问题仍然存在

如果上述解决方案仍然无法解决问题，请尝试以下步骤：

1. **检查 Pandoc 版本**：

   ```bash
   pandoc --version
   ```

   建议使用 Pandoc 2.19 或更高版本。

1. **检查 Markdown 源内容**：
   - 导出为 Markdown 格式
   - 检查是否包含了错误的 HTML 标签或样式
   - 手动移除这些标签后重新转换

1. **使用不同的 PDF 引擎**：
   - 系统会自动尝试多个 PDF 引擎：`wkhtmltopdf`、`weasyprint`、默认引擎
   - 检查日志，看看使用了哪个引擎
   - 尝试安装其他 PDF 引擎

1. **检查字体**：
   - 确保系统安装了 `Noto Sans CJK SC` 字体
   - 或者修改 `extra_args` 中的字体设置

- --

## 问题 2: 表格跨页被截断

### 问题描述

在将 Markdown 报告导出为 PDF 或 Word 文档时，表格在页面边界被截断，内容跨页显示不完整。

### 解决方案

#### 1. 添加 CSS 分页控制（已实现）

在 `_create_pdf_css()` 方法中，添加了表格分页控制：

```css
/*表格样式 - 允许跨页*/
table {
    width: 100%;
    border-collapse: collapse;
    page-break-inside: auto;
}

/*表格行 - 避免在行中间分页*/
tr {
    page-break-inside: avoid;
    page-break-after: auto;
}

/*表头 - 在每页重复显示*/
thead {
    display: table-header-group;
}

```bash

#### 2. 设置页边距（已实现）

在 PDF 生成参数中添加了页边距设置：

```python
'-V', 'geometry:margin=2cm',  # 设置页边距

```bash

### 测试方法

1. 生成一份包含大型表格的报告
2. 导出为 PDF 或 Word
3. 检查表格是否能够正确跨页显示
4. 检查表头是否在每页重复显示

- --

## 相关文件

- `app/utils/report_exporter.py` - 报告导出核心逻辑
- `web/utils/report_exporter.py` - Web 版本的报告导出
- `app/routers/reports.py` - 报告 API 路由

## 相关依赖

- `pypandoc` - Pandoc Python 接口
- `pandoc` - 文档转换工具
- `python-docx` - Word 文档处理库
- `wkhtmltopdf` / `weasyprint` - PDF 生成引擎

## 更新日志

- **2025-11-05**: 添加中文竖排问题的解决方案
- **2025-11-05**: 添加表格分页控制
- **2025-11-05**: 添加 Word 文档后处理逻辑
