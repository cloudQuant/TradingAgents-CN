"""
自动生成股票接口需求文档
"""
import re
from pathlib import Path

def extract_interface_info(html_file):
    """从HTML文件中提取接口的详细信息"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割成块
    lines = content.split('\n')
    interfaces = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 找到接口定义
        if line.startswith('接口:'):
            interface_info = {}
            interface_info['name'] = line.split(':', 1)[1].strip()
            
            # 向上查找章节标题
            section_lines = []
            for j in range(i-1, max(0, i-10), -1):
                if lines[j].startswith('###') or lines[j].startswith('####') or lines[j].startswith('#####'):
                    section_lines.append(lines[j].strip().lstrip('#').strip())
                    if len(section_lines) >= 3:
                        break
            interface_info['sections'] = list(reversed(section_lines))
            if section_lines:
                interface_info['title'] = section_lines[0]  # 最近的标题
            
            # 向下查找详细信息
            j = i + 1
            description_found = False
            in_params = False
            input_params = []
            output_params = []
            example_code = []
            in_example = False
            
            while j < len(lines) and j < i + 200:  # 最多向下查找200行
                current_line = lines[j]
                
                # 遇到下一个接口定义，停止
                if current_line.startswith('接口:'):
                    break
                
                # 目标地址
                if current_line.startswith('目标地址:'):
                    interface_info['url'] = current_line.split(':', 1)[1].strip()
                
                # 描述
                if current_line.startswith('描述:'):
                    interface_info['description'] = current_line.split(':', 1)[1].strip()
                    description_found = True
                
                # 限量
                if current_line.startswith('限量:'):
                    interface_info['limit'] = current_line.split(':', 1)[1].strip()
                
                # 输入参数表格
                if '输入参数' in current_line:
                    in_params = True
                    param_type = 'input'
                elif '输出参数' in current_line:
                    in_params = True
                    param_type = 'output'
                elif in_params and current_line.startswith('|') and '---' not in current_line and '名称' not in current_line:
                    # 解析表格行
                    parts = [p.strip() for p in current_line.split('|') if p.strip()]
                    if len(parts) >= 2:
                        if param_type == 'input':
                            input_params.append(parts)
                        else:
                            output_params.append(parts)
                elif in_params and (current_line.startswith('接口示例') or current_line.startswith('数据示例') or current_line.startswith('```')):
                    in_params = False
                
                # 接口示例
                if '接口示例' in current_line or (current_line.startswith('```python') and not in_example):
                    in_example = True
                elif in_example:
                    if current_line.startswith('```') and example_code:
                        in_example = False
                    elif not current_line.startswith('```'):
                        example_code.append(current_line)
                
                j += 1
            
            interface_info['input_params'] = input_params
            interface_info['output_params'] = output_params
            interface_info['example_code'] = '\n'.join(example_code) if example_code else ''
            
            interfaces.append(interface_info)
        
        i += 1
    
    return interfaces

def generate_requirement_doc(interface_info, index, is_detailed=False):
    """生成需求文档内容"""
    name = interface_info['name']
    title = interface_info.get('title', name)
    description = interface_info.get('description', '')
    url = interface_info.get('url', '')
    limit = interface_info.get('limit', '')
    input_params = interface_info.get('input_params', [])
    output_params = interface_info.get('output_params', [])
    example_code = interface_info.get('example_code', '')
    
    # 生成文档内容
    doc = f"""### 背景
{description}

### 任务

参考债券数据集合bond_info_cm和基金数据集合的前端界面和后端实现的功能，参考下面获取数据的API接口和字段，获取数据并建立数据集合。

### 步骤
1. 数据集合：创建一个新的数据集合，名称为**{title}** (http://localhost:3000/stocks/collections/{name})
2. 页面里面需要包含数据概览、数据列表、刷新、清空数据、更新数据等功能，根据后端获取到的数据和数据列表里面的数据，增加一些基本的图形展示，让整个页面更加美观
3. 更新数据这个功能需要支持：
   - **文件导入**：支持CSV/Excel文件导入
   - **远程同步**：从其他数据库同步数据
"""
    
    # 根据接口特点决定是否需要批量更新
    if input_params and any('symbol' in str(p).lower() or 'code' in str(p).lower() for p in input_params):
        doc += """   - **批量更新**：从其他数据集合获取代码列表，批量获取数据
   - **单个更新**：输入代码，单独更新数据
4. 数据唯一标识：根据接口特点确定唯一标识字段（如代码、日期等）
"""
    else:
        doc += """   - **更新**：一次性获取所有数据（API一次返回所有数据）
4. 数据唯一标识：根据数据特点确定唯一标识字段
"""
    
    doc += f"""
### 测试驱动
1. 需要认真思考研究债券数据集合bond_info_cm和基金数据集合的前端界面和后端实现的功能，结合该接口的字段，思考需要实现哪些功能，先写具体的测试用例
2. 测试用例文件：`tests/stocks/collections/{index:03d}_{name}_collection.py`
3. 开发实现相应的前端和后端功能
4. 运行测试，修复测试失败的问题

### 验收标准
1. 测试用例能够全部通过
2. 手动点击没有异常情况
3. 数据能够正确获取、存储和展示
4. 页面美观、交互流畅

### 获取数据的API接口、字段等

#### {title}

**接口**: `{name}`

"""
    
    if url:
        doc += f"**目标地址**: {url}\n\n"
    
    if description:
        doc += f"**描述**: {description}\n\n"
    
    if limit:
        doc += f"**限量**: {limit}\n\n"
    
    # 输入参数
    if input_params:
        doc += "**输入参数**\n\n"
        doc += "| 名称 | 类型 | 描述 |\n"
        doc += "|-----|-----|-----|\n"
        for param in input_params:
            if len(param) >= 3:
                doc += f"| {param[0]} | {param[1]} | {param[2]} |\n"
            elif len(param) == 2:
                doc += f"| {param[0]} | {param[1]} | - |\n"
        doc += "\n"
    else:
        doc += "**输入参数**\n\n"
        doc += "| 名称 | 类型 | 描述 |\n"
        doc += "|-----|-----|-----|\n"
        doc += "| - | - | - |\n\n"
    
    # 输出参数
    if output_params:
        doc += "**输出参数**\n\n"
        doc += "| 名称 | 类型 | 描述 |\n"
        doc += "|-----|-----|-----|\n"
        for param in output_params:
            if len(param) >= 3:
                doc += f"| {param[0]} | {param[1]} | {param[2]} |\n"
            elif len(param) == 2:
                doc += f"| {param[0]} | {param[1]} | - |\n"
        doc += "\n"
    
    # 接口示例
    if example_code:
        doc += "**接口示例**\n\n"
        doc += "```python\n"
        doc += example_code.strip()
        doc += "\n```\n\n"
    
    # 实现要点（简化版）
    doc += """### 实现要点

1. **后端实现**：
   - 实现数据获取、存储、更新逻辑
   - 实现文件导入和远程同步功能
   - 注意API调用频率控制

2. **前端实现**：
   - 参考现有集合的布局
   - 实现数据概览、列表、更新等组件
   - 增加适当的数据可视化

3. **注意事项**：
   - 数据验证和清洗
   - 错误处理和日志记录
   - 性能优化（批量操作、索引等）
"""
    
    return doc

if __name__ == '__main__':
    html_file = Path(__file__).parent / '_sources_data_stock_stock.md.txt.html'
    output_dir = Path(__file__).parent / 'requirements'
    output_dir.mkdir(exist_ok=True)
    
    print("正在提取接口信息...")
    interfaces = extract_interface_info(html_file)
    print(f"共提取到 {len(interfaces)} 个接口\n")
    
    # 生成需求文档
    print("正在生成需求文档...")
    for i, interface_info in enumerate(interfaces, 1):
        name = interface_info['name']
        title = interface_info.get('title', name)
        
        # 生成文档内容
        doc_content = generate_requirement_doc(interface_info, i + 6)  # 从7开始编号（前6个已有）
        
        # 保存文档
        filename = f"{i+6:02d}_{title}.md"
        # 清理文件名中的非法字符
        filename = filename.replace('/', '-').replace('\\', '-').replace(':', '-')
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        if i <= 10 or i % 50 == 0:
            print(f"  [{i}/{len(interfaces)}] 已生成: {filename}")
    
    print(f"\n✅ 所有需求文档已生成到: {output_dir}")
    print(f"   共生成 {len(interfaces)} 个需求文档")
