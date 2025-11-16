"""
验证数据集合顺序和显示名称
确保债券信息查询在第一位
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

print("=" * 60)
print("验证数据集合配置")
print("=" * 60)

# 1. 读取bonds.py文件验证配置
bonds_router_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'app', 'routers', 'bonds.py'
)
bonds_router_path = os.path.abspath(bonds_router_path)

print(f"\n[检查1] 读取配置文件: {bonds_router_path}")

with open(bonds_router_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找collections列表
collections_start = content.find('collections = [')
if collections_start < 0:
    print("  [FAILED] 找不到collections列表")
    sys.exit(1)

# 提取第一个collection
first_collection_start = content.find('{', collections_start)
first_collection_end = content.find('},', first_collection_start)
first_collection = content[first_collection_start:first_collection_end]

print("\n[检查2] 验证第一个集合配置")

# 检查name
if '"name": "bond_info_cm"' in first_collection:
    print("  [OK] name: bond_info_cm")
else:
    print("  [FAILED] name不是bond_info_cm")
    sys.exit(1)

# 检查display_name
if '"display_name": "债券信息查询"' in first_collection:
    print("  [OK] display_name: 债券信息查询")
else:
    print("  [FAILED] display_name不正确")
    sys.exit(1)

# 检查route
if '"route": "/bonds/collections/bond_info_cm"' in first_collection:
    print("  [OK] route: /bonds/collections/bond_info_cm")
else:
    print("  [FAILED] route不正确")

print("\n[检查3] 验证侧边栏菜单顺序")

sidebar_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
)
sidebar_path = os.path.abspath(sidebar_path)

with open(sidebar_path, 'r', encoding='utf-8') as f:
    sidebar_content = f.read()

# 查找债券分析子菜单
bonds_submenu_start = sidebar_content.find('<el-sub-menu index="/bonds">')
if bonds_submenu_start < 0:
    print("  [FAILED] 找不到债券分析子菜单")
    sys.exit(1)

bonds_submenu_end = sidebar_content.find('</el-sub-menu>', bonds_submenu_start)
bonds_submenu = sidebar_content[bonds_submenu_start:bonds_submenu_end]

# 提取菜单项顺序
menu_items = []
import re
pattern = r'<el-menu-item index="([^"]+)">([^<]+)</el-menu-item>'
matches = re.findall(pattern, bonds_submenu)

print("\n  债券分析子菜单顺序:")
for i, (route, label) in enumerate(matches, 1):
    menu_items.append((route, label))
    print(f"    {i}. {label} ({route})")

# 验证顺序
expected_order = [
    ('/bonds/overview', '概览'),
    ('/bonds/collections', '数据集合'),
    ('/bonds/analysis', '债券分析'),
    ('/bonds/yield-curve', '收益率曲线')
]

if menu_items == expected_order:
    print("\n  [OK] 菜单顺序正确: 概览 -> 数据集合 -> 债券分析 -> 收益率曲线")
else:
    print("\n  [FAILED] 菜单顺序不正确")
    print(f"    预期: {expected_order}")
    print(f"    实际: {menu_items}")

print("\n" + "=" * 60)
print("[SUCCESS] 所有检查通过！")
print("=" * 60)
print("\n配置摘要:")
print("  - 第一个数据集合: 债券信息查询 (bond_info_cm)")
print("  - 侧边栏菜单顺序: 概览 -> 数据集合 -> 债券分析 -> 收益率曲线")
print("\n访问路径:")
print("  1. 数据集合列表: /bonds/collections")
print("  2. 债券信息查询: /bonds/collections/bond_info_cm")
print("\n提示: 如果前端页面没有更新，请清除浏览器缓存或强制刷新(Ctrl+F5)")
