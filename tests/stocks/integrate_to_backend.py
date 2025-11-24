"""
自动整合生成的代码到后端文件
"""
from pathlib import Path
import re

# 项目根目录
project_root = Path(__file__).parent.parent.parent
stocks_router_file = project_root / "app" / "routers" / "stocks.py"

print("开始整合代码到后端...")
print(f"目标文件: {stocks_router_file}")

# 读取当前的 stocks.py
content = stocks_router_file.read_text(encoding='utf-8')

# 读取生成的API路由
api_routes_file = Path(__file__).parent / "generated_api_routes.py"
if not api_routes_file.exists():
    print("错误: generated_api_routes.py 不存在")
    exit(1)

api_routes_content = api_routes_file.read_text(encoding='utf-8')

# 读取生成的集合注册
collections_file = Path(__file__).parent / "generated_collections_registration.py"
if not collections_file.exists():
    print("错误: generated_collections_registration.py 不存在")
    exit(1)

collections_content = collections_file.read_text(encoding='utf-8')

# 提取API路由代码（去掉注释和文档字符串）
api_routes_match = re.search(r'# 将以下代码添加到.*?\n\n(.+)', api_routes_content, re.DOTALL)
if api_routes_match:
    api_routes_to_add = api_routes_match.group(1).strip()
else:
    print("警告: 无法提取API路由代码")
    api_routes_to_add = ""

# 提取集合注册代码
collections_match = re.search(r'collections = \[(.*?)\]', collections_content, re.DOTALL)
if collections_match:
    collections_to_add = collections_match.group(1).strip()
else:
    print("警告: 无法提取集合注册代码")
    collections_to_add = ""

# 查找 collections 列表的位置
# 查找类似 collections = [ 或 collections = [] 的模式
collections_pattern = r'(collections\s*=\s*\[)(.*?)(\])'
collections_search = re.search(collections_pattern, content, re.DOTALL)

if collections_search:
    print("找到 collections 列表")
    existing_collections = collections_search.group(2).strip()
    
    # 在现有集合后添加新集合
    if existing_collections:
        new_collections = f"{existing_collections},\n{collections_to_add}"
    else:
        new_collections = collections_to_add
    
    # 替换集合列表
    new_content = re.sub(
        collections_pattern,
        rf'\1\n{new_collections}\n\3',
        content,
        flags=re.DOTALL
    )
    
    print(f"添加了 290 个新集合到 collections 列表")
else:
    print("警告: 未找到 collections 列表，将在文件末尾添加")
    new_content = content + f"\n\n# 新增集合列表\ncollections = [\n{collections_to_add}\n]\n"

# 在文件末尾添加API路由
if api_routes_to_add:
    new_content += f"\n\n# ========== 自动生成的API路由 (290个集合 x 4个端点) ==========\n\n{api_routes_to_add}\n"
    print("添加了 1160 个新的API端点")

# 备份原文件
backup_file = stocks_router_file.with_suffix('.py.backup')
stocks_router_file.rename(backup_file)
print(f"原文件已备份到: {backup_file}")

# 写入新内容
stocks_router_file.write_text(new_content, encoding='utf-8')
print(f"已更新 {stocks_router_file}")

print("\n" + "="*80)
print("整合完成！")
print("="*80)
print("\n后续步骤:")
print("1. 检查 app/routers/stocks.py 文件确认修改正确")
print("2. 创建 app/services/stock/providers/__init__.py")
print("3. 重启后端服务")
print("4. 访问 http://localhost:8848/api/stocks/collections 验证")
print("="*80)
