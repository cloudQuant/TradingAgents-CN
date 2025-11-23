"""
提取股票接口列表并生成需求文档结构
"""
import re
from pathlib import Path

def extract_interfaces(html_file):
    """从HTML文件中提取所有接口信息"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有接口定义
    # 格式：接口: interface_name
    pattern = r'接口:\s*(\w+)'
    interfaces = re.findall(pattern, content)
    
    # 去重并保持顺序
    seen = set()
    unique_interfaces = []
    for interface in interfaces:
        if interface not in seen:
            seen.add(interface)
            unique_interfaces.append(interface)
    
    return unique_interfaces

def extract_interface_details(html_file):
    """提取接口的详细信息"""
    with open(html_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    interfaces_details = []
    current_interface = {}
    in_interface_block = False
    section_title = ""
    
    for i, line in enumerate(lines):
        # 检测章节标题
        if line.startswith('###') or line.startswith('####') or line.startswith('#####'):
            # 提取标题（去掉井号和空格）
            section_title = line.strip().lstrip('#').strip()
        
        # 检测接口定义
        if line.startswith('接口:'):
            # 保存上一个接口
            if current_interface:
                interfaces_details.append(current_interface)
            
            # 开始新接口
            interface_name = line.split(':')[1].strip()
            current_interface = {
                'name': interface_name,
                'section': section_title,
                'line_number': i + 1
            }
            in_interface_block = True
            continue
        
        # 提取目标地址
        if in_interface_block and line.startswith('目标地址:'):
            current_interface['url'] = line.split(':', 1)[1].strip()
        
        # 提取描述
        if in_interface_block and line.startswith('描述:'):
            current_interface['description'] = line.split(':', 1)[1].strip()
        
        # 检测接口块结束（遇到下一个标题或接口）
        if in_interface_block and (line.startswith('###') or line.startswith('####') or line.startswith('#####') or line.startswith('接口:')):
            if not line.startswith('接口:'):
                in_interface_block = False
    
    # 保存最后一个接口
    if current_interface:
        interfaces_details.append(current_interface)
    
    return interfaces_details

if __name__ == '__main__':
    html_file = Path(__file__).parent / '_sources_data_stock_stock.md.txt.html'
    
    # 提取接口列表
    interfaces = extract_interfaces(html_file)
    print(f"总共找到 {len(interfaces)} 个接口\n")
    
    # 提取详细信息
    details = extract_interface_details(html_file)
    
    # 按类别组织
    categories = {}
    for detail in details:
        section = detail.get('section', '未分类')
        if section not in categories:
            categories[section] = []
        categories[section].append(detail)
    
    # 输出统计
    print(f"按类别统计：")
    for category, items in categories.items():
        print(f"  {category}: {len(items)}个接口")
    
    print("\n" + "="*80 + "\n")
    
    # 输出详细列表
    print("接口详细列表：\n")
    for i, detail in enumerate(details, 1):
        print(f"{i:3d}. {detail['name']}")
        print(f"     章节: {detail.get('section', 'N/A')}")
        if 'description' in detail:
            print(f"     描述: {detail['description']}")
        print()
    
    # 保存到文件
    output_file = Path(__file__).parent / 'interface_list.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"股票数据接口列表（共{len(details)}个）\n")
        f.write("="*80 + "\n\n")
        
        for category, items in sorted(categories.items()):
            f.write(f"\n## {category} ({len(items)}个接口)\n\n")
            for item in items:
                f.write(f"- {item['name']}")
                if 'description' in item:
                    f.write(f" - {item['description']}")
                f.write("\n")
    
    print(f"\n详细列表已保存到: {output_file}")
