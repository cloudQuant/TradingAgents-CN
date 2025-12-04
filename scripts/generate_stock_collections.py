#!/usr/bin/env python
"""
批量生成股票数据集合的Provider和Service文件

根据需求文档自动生成符合funds模式的代码

使用方法:
    python scripts/generate_stock_collections.py
"""
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
REQUIREMENTS_DIR = PROJECT_ROOT / "tests" / "stocks" / "requirements"
PROVIDERS_DIR = PROJECT_ROOT / "app" / "services" / "data_sources" / "stocks" / "providers"
SERVICES_DIR = PROJECT_ROOT / "app" / "services" / "data_sources" / "stocks" / "services"


def parse_requirement_doc(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    解析需求文档，提取集合信息
    
    返回:
        {
            'collection_name': 'stock_xxx',
            'display_name': '显示名称',
            'description': '描述',
            'akshare_func': 'stock_xxx',
            'input_params': [{'name': 'symbol', 'type': 'str', 'description': '...'}],
            'output_fields': [{'name': '代码', 'type': 'object', 'description': '...'}],
            'unique_keys': ['代码'],
        }
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None
    
    result = {
        'collection_name': '',
        'display_name': '',
        'description': '',
        'akshare_func': '',
        'input_params': [],
        'output_fields': [],
        'unique_keys': [],
    }
    
    # 提取接口名称
    func_match = re.search(r'\*\*接口\*\*:\s*`([^`]+)`', content)
    if func_match:
        result['akshare_func'] = func_match.group(1)
        result['collection_name'] = func_match.group(1)
    
    # 提取显示名称（从标题或文件名）
    title_match = re.search(r'####\s+(.+?)(?:\n|$)', content)
    if title_match:
        result['display_name'] = title_match.group(1).strip()
    else:
        # 从文件名提取
        filename = filepath.stem
        # 去掉序号和状态后缀
        name = re.sub(r'^\d+_', '', filename)
        name = re.sub(r'-(?:finished|完成|完整)$', '', name)
        result['display_name'] = name
    
    # 提取描述
    desc_match = re.search(r'\*\*描述\*\*:\s*(.+?)(?:\n|$)', content)
    if desc_match:
        result['description'] = desc_match.group(1).strip()
    else:
        result['description'] = result['display_name']
    
    # 提取输入参数
    # 可选参数列表（不应该作为必填参数）
    optional_params = {'timeout', 'adjust', 'verbose', 'retry'}
    
    input_section = re.search(r'\*\*输入参数\*\*\s*\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)*)', content)
    if input_section:
        rows = input_section.group(1).strip().split('\n')
        for row in rows:
            cols = [c.strip() for c in row.split('|')[1:-1]]
            if len(cols) >= 3 and cols[0] != '-':
                param_name = cols[0]
                is_optional = param_name in optional_params or '默认' in cols[2] if len(cols) > 2 else False
                result['input_params'].append({
                    'name': param_name,
                    'type': cols[1],
                    'description': cols[2] if len(cols) > 2 else '',
                    'optional': is_optional
                })
    
    # 提取输出参数
    output_section = re.search(r'\*\*输出参数\*\*\s*\n\n\|[^\n]+\n\|[^\n]+\n((?:\|[^\n]+\n)*)', content)
    if output_section:
        rows = output_section.group(1).strip().split('\n')
        for row in rows:
            cols = [c.strip() for c in row.split('|')[1:-1]]
            if len(cols) >= 2:
                result['output_fields'].append({
                    'name': cols[0],
                    'type': cols[1] if len(cols) > 1 else 'object',
                    'description': cols[2] if len(cols) > 2 else ''
                })
    
    # 确定唯一键
    unique_keys = []
    # 先从文档中查找唯一标识说明
    unique_match = re.search(r'数据唯一标识[：:]\s*以?\*?\*?([^*\n]+)', content)
    if unique_match:
        key_text = unique_match.group(1)
        # 提取字段名（在**之间或"和"之间）
        keys = re.findall(r'[「【]?(\w+)[」】]?', key_text)
        for key in keys:
            if key in ['代码', '股票代码', '日期', '序号', '板块', '板块名称', '行业']:
                unique_keys.append(key)
    
    # 默认唯一键逻辑
    if not unique_keys:
        field_names = [f['name'] for f in result['output_fields']]
        if '代码' in field_names:
            unique_keys.append('代码')
        elif '股票代码' in field_names:
            unique_keys.append('股票代码')
        if '日期' in field_names and 'hist' in result['collection_name']:
            unique_keys.append('日期')
    
    if not unique_keys:
        unique_keys = ['代码'] if result['output_fields'] else []
    
    result['unique_keys'] = unique_keys
    
    return result if result['collection_name'] else None


def snake_to_pascal(name: str) -> str:
    """将下划线命名转换为帕斯卡命名"""
    return ''.join(word.capitalize() for word in name.split('_'))


def generate_provider_code(info: Dict[str, Any]) -> str:
    """生成Provider代码"""
    collection_name = info['collection_name']
    class_name = snake_to_pascal(collection_name) + 'Provider'
    display_name = info['display_name']
    description = info['description']
    akshare_func = info['akshare_func']
    unique_keys = info['unique_keys']
    input_params = info['input_params']
    output_fields = info['output_fields']
    
    # 确定是SimpleProvider还是BaseProvider
    has_required_params = any(p.get('name') != '-' for p in input_params)
    base_class = 'BaseProvider' if has_required_params else 'SimpleProvider'
    
    # 生成字段信息
    field_info_lines = []
    for field in output_fields:
        field_info_lines.append(
            f'        {{"name": "{field["name"]}", "type": "{field.get("type", "object")}", "description": "{field.get("description", "")}"}}'
        )
    field_info_lines.append('        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"}')
    field_info_str = ',\n'.join(field_info_lines)
    
    # 生成参数映射
    param_mapping_lines = []
    required_params = []
    if has_required_params:
        for param in input_params:
            if param['name'] != '-':
                param_name = param['name']
                param_mapping_lines.append(f'        "{param_name}": "{param_name}"')
                # 常见别名
                if param_name == 'symbol':
                    param_mapping_lines.append(f'        "code": "symbol"')
                    param_mapping_lines.append(f'        "stock_code": "symbol"')
                # 只有非可选参数才加入required_params
                if not param.get('optional', False):
                    required_params.append(param_name)
    
    param_mapping_str = ',\n'.join(param_mapping_lines) if param_mapping_lines else ''
    required_params_str = str(required_params)
    
    # 确定集合类别
    category = "默认"
    if 'spot' in collection_name or '实时' in display_name:
        category = "实时行情"
    elif 'hist' in collection_name or '历史' in display_name:
        category = "历史行情"
    elif 'board' in collection_name or '板块' in display_name:
        category = "板块数据"
    elif 'fund_flow' in collection_name or '资金' in display_name:
        category = "资金流向"
    elif 'lhb' in collection_name or '龙虎榜' in display_name:
        category = "龙虎榜"
    elif 'hsgt' in collection_name or '沪深港通' in display_name:
        category = "沪深港通"
    elif 'financial' in collection_name or '财务' in display_name:
        category = "财务数据"
    elif 'hot' in collection_name or '热门' in display_name:
        category = "热门排行"
    
    code = f'''"""
{display_name}数据提供者

{description}
接口: {akshare_func}
"""
from app.services.data_sources.base_provider import {base_class}


class {class_name}({base_class}):
    """{display_name}数据提供者"""
    
    # 必填属性
    collection_name = "{collection_name}"
    display_name = "{display_name}"
    akshare_func = "{akshare_func}"
    unique_keys = {unique_keys}
    
    # 可选属性
    collection_description = "{description}"
    collection_route = "/stocks/collections/{collection_name}"
    collection_category = "{category}"
'''
    
    # 添加参数映射（如果需要）
    if has_required_params and param_mapping_str:
        code += f'''
    # 参数映射
    param_mapping = {{
{param_mapping_str}
    }}
    
    # 必填参数
    required_params = {required_params_str}
'''
    
    # 添加字段信息
    if field_info_str:
        code += f'''
    # 字段信息
    field_info = [
{field_info_str},
    ]
'''
    
    return code


def generate_service_code(info: Dict[str, Any]) -> str:
    """生成Service代码"""
    collection_name = info['collection_name']
    class_name = snake_to_pascal(collection_name) + 'Service'
    provider_class_name = snake_to_pascal(collection_name) + 'Provider'
    display_name = info['display_name']
    description = info['description']
    input_params = info['input_params']
    
    # 确定是SimpleService还是BaseService
    has_required_params = any(p.get('name') != '-' for p in input_params)
    base_class = 'BaseService' if has_required_params else 'SimpleService'
    
    code = f'''"""
{display_name}服务

{description}
接口: {collection_name}
"""
from app.services.data_sources.base_service import {base_class}
from ..providers.{collection_name}_provider import {provider_class_name}


class {class_name}({base_class}):
    """{display_name}服务"""
    
    collection_name = "{collection_name}"
    provider_class = {provider_class_name}
    
    # 时间字段名
    time_field = "更新时间"
'''
    
    return code


def process_all_requirements():
    """处理所有需求文档，生成Provider和Service"""
    # 确保目录存在
    PROVIDERS_DIR.mkdir(parents=True, exist_ok=True)
    SERVICES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 获取所有需求文档
    requirement_files = sorted(REQUIREMENTS_DIR.glob("*.md"))
    
    # 过滤掉非需求文档
    excluded_files = {
        'API_UPDATE_IMPLEMENTATION_GUIDE.md',
        'API_UPDATE_PROGRESS.md', 
        'CURRENT_STATUS_SUMMARY.md',
        'CUSTOMIZED_API_UPDATE_COMPLETE.md',
        'IMPLEMENTATION_COMPLETE.md',
        'IMPLEMENTATION_STATUS.md',
        'NEXT_STEPS.md',
        'QUICK_TEST_GUIDE.md',
        'README.md',
        'README_API_UPDATE.md',
    }
    
    requirement_files = [f for f in requirement_files if f.name not in excluded_files]
    
    print(f"找到 {len(requirement_files)} 个需求文档")
    
    success_count = 0
    failed_files = []
    generated_collections = []
    
    for filepath in requirement_files:
        info = parse_requirement_doc(filepath)
        
        if not info or not info['collection_name']:
            failed_files.append((filepath.name, "无法解析集合名称"))
            continue
        
        collection_name = info['collection_name']
        
        # 生成Provider
        provider_code = generate_provider_code(info)
        provider_file = PROVIDERS_DIR / f"{collection_name}_provider.py"
        
        try:
            with open(provider_file, 'w', encoding='utf-8') as f:
                f.write(provider_code)
        except Exception as e:
            failed_files.append((filepath.name, f"写入Provider失败: {e}"))
            continue
        
        # 生成Service
        service_code = generate_service_code(info)
        service_file = SERVICES_DIR / f"{collection_name}_service.py"
        
        try:
            with open(service_file, 'w', encoding='utf-8') as f:
                f.write(service_code)
        except Exception as e:
            failed_files.append((filepath.name, f"写入Service失败: {e}"))
            continue
        
        generated_collections.append(collection_name)
        success_count += 1
        
        if success_count % 50 == 0:
            print(f"已处理 {success_count} 个集合...")
    
    # 更新__init__.py
    providers_init = PROVIDERS_DIR / "__init__.py"
    with open(providers_init, 'w', encoding='utf-8') as f:
        f.write('"""股票数据Provider模块"""\n')
    
    services_init = SERVICES_DIR / "__init__.py"
    with open(services_init, 'w', encoding='utf-8') as f:
        f.write('"""股票数据Service模块"""\n')
    
    print(f"\n生成完成!")
    print(f"成功: {success_count} 个集合")
    print(f"失败: {len(failed_files)} 个文件")
    
    if failed_files:
        print("\n失败的文件:")
        for filename, reason in failed_files[:20]:
            print(f"  - {filename}: {reason}")
        if len(failed_files) > 20:
            print(f"  ... 还有 {len(failed_files) - 20} 个")
    
    return generated_collections


if __name__ == "__main__":
    collections = process_all_requirements()
    print(f"\n生成了 {len(collections)} 个集合")
