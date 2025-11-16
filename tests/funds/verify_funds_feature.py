"""
手动验证基金投研功能
不使用pytest，直接运行检查
"""
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

print("="*70)
print("基金投研功能验证")
print("="*70)

# 1. 检查侧边栏菜单
print("\n[检查1] 验证侧边栏是否有基金投研菜单")
sidebar_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'components', 'Layout', 'SidebarMenu.vue'
)
sidebar_path = os.path.abspath(sidebar_path)

if not os.path.exists(sidebar_path):
    print(f"  [FAILED] 侧边栏文件不存在: {sidebar_path}")
    sys.exit(1)

with open(sidebar_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查基金投研菜单
if 'index="/funds"' not in content:
    print("  [FAILED] 侧边栏中找不到基金投研菜单 (index=\"/funds\")")
    sys.exit(1)
else:
    print("  [OK] 找到基金投研菜单")

if '基金投研' not in content:
    print("  [FAILED] 侧边栏中找不到'基金投研'文本")
    sys.exit(1)
else:
    print("  [OK] 找到'基金投研'文本")

# 检查子菜单
funds_start = content.find('index="/funds"')
funds_end = content.find('</el-sub-menu>', funds_start)
funds_block = content[funds_start:funds_end]

if 'index="/funds/overview"' not in funds_block:
    print("  [FAILED] 找不到概览选项")
    sys.exit(1)
else:
    print("  [OK] 找到概览选项")

if 'index="/funds/collections"' not in funds_block:
    print("  [FAILED] 找不到数据集合选项")
    sys.exit(1)
else:
    print("  [OK] 找到数据集合选项")

if 'index="/funds/analysis"' not in funds_block:
    print("  [FAILED] 找不到基金分析选项")
    sys.exit(1)
else:
    print("  [OK] 找到基金分析选项")

# 2. 检查路由配置
print("\n[检查2] 验证路由配置")
router_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'router', 'index.ts'
)
router_path = os.path.abspath(router_path)

if not os.path.exists(router_path):
    print(f"  [FAILED] 路由文件不存在: {router_path}")
    sys.exit(1)

with open(router_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "path: '/funds'" not in content:
    print("  [FAILED] 路由配置中找不到 /funds 路径")
    sys.exit(1)
else:
    print("  [OK] 找到 /funds 路由")

if "path: 'overview'" not in content and "'overview'" not in content:
    print("  [FAILED] 路由配置中找不到 overview 子路由")
    sys.exit(1)
else:
    print("  [OK] 找到 overview 子路由")

if "path: 'collections'" not in content and "'collections'" not in content:
    print("  [FAILED] 路由配置中找不到 collections 子路由")
    sys.exit(1)
else:
    print("  [OK] 找到 collections 子路由")

if "path: 'analysis'" not in content and "'analysis'" not in content:
    print("  [FAILED] 路由配置中找不到 analysis 子路由")
    sys.exit(1)
else:
    print("  [OK] 找到 analysis 子路由")

# 3. 检查前端页面文件
print("\n[检查3] 验证前端页面文件")

overview_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'views', 'Funds', 'index.vue'
)
overview_path = os.path.abspath(overview_path)

if not os.path.exists(overview_path):
    print(f"  [FAILED] 基金概览页面文件不存在: {overview_path}")
    sys.exit(1)
else:
    print("  [OK] 基金概览页面文件存在")

collections_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'views', 'Funds', 'Collections.vue'
)
collections_path = os.path.abspath(collections_path)

if not os.path.exists(collections_path):
    print(f"  [FAILED] 基金数据集合页面文件不存在: {collections_path}")
    sys.exit(1)
else:
    print("  [OK] 基金数据集合页面文件存在")

analysis_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'views', 'Funds', 'FundAnalysis.vue'
)
analysis_path = os.path.abspath(analysis_path)

if not os.path.exists(analysis_path):
    print(f"  [FAILED] 基金分析页面文件不存在: {analysis_path}")
    sys.exit(1)
else:
    print("  [OK] 基金分析页面文件存在")

# 4. 检查API文件
print("\n[检查4] 验证API文件")
api_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'frontend', 'src', 'api', 'funds.ts'
)
api_path = os.path.abspath(api_path)

if not os.path.exists(api_path):
    print(f"  [FAILED] API文件不存在: {api_path}")
    sys.exit(1)
else:
    print("  [OK] API文件存在")

with open(api_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'getOverview' not in content:
    print("  [FAILED] API文件中找不到 getOverview 方法")
    sys.exit(1)
else:
    print("  [OK] 找到 getOverview 方法")

if 'getCollections' not in content:
    print("  [FAILED] API文件中找不到 getCollections 方法")
    sys.exit(1)
else:
    print("  [OK] 找到 getCollections 方法")

if 'getFundAnalysis' not in content:
    print("  [FAILED] API文件中找不到 getFundAnalysis 方法")
    sys.exit(1)
else:
    print("  [OK] 找到 getFundAnalysis 方法")

# 5. 检查后端路由
print("\n[检查5] 验证后端路由")
backend_router_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'app', 'routers', 'funds.py'
)
backend_router_path = os.path.abspath(backend_router_path)

if not os.path.exists(backend_router_path):
    print(f"  [FAILED] 后端路由文件不存在: {backend_router_path}")
    sys.exit(1)
else:
    print("  [OK] 后端路由文件存在")

with open(backend_router_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'APIRouter' not in content:
    print("  [FAILED] 路由文件中找不到 APIRouter")
    sys.exit(1)
else:
    print("  [OK] 找到 APIRouter")

if '/api/funds' not in content:
    print("  [FAILED] 路由文件中找不到 /api/funds 前缀")
    sys.exit(1)
else:
    print("  [OK] 找到 /api/funds 前缀")

if '@router.get("/overview")' not in content:
    print("  [FAILED] 找不到 /overview 端点")
    sys.exit(1)
else:
    print("  [OK] 找到 /overview 端点")

if '@router.get("/collections")' not in content:
    print("  [FAILED] 找不到 /collections 端点")
    sys.exit(1)
else:
    print("  [OK] 找到 /collections 端点")

# 6. 检查main.py中的路由注册
print("\n[检查6] 验证后端路由注册")
main_path = os.path.join(
    os.path.dirname(__file__), 
    '..', '..', 'app', 'main.py'
)
main_path = os.path.abspath(main_path)

if not os.path.exists(main_path):
    print(f"  [FAILED] main.py文件不存在: {main_path}")
    sys.exit(1)

with open(main_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'from app.routers import funds as funds_router' not in content:
    print("  [FAILED] main.py中找不到基金路由的导入")
    sys.exit(1)
else:
    print("  [OK] main.py中找到基金路由的导入")

if 'app.include_router(funds_router.router)' not in content:
    print("  [FAILED] main.py中找不到基金路由的注册")
    sys.exit(1)
else:
    print("  [OK] main.py中找到基金路由的注册")

print("\n" + "="*70)
print("[SUCCESS] 所有检查通过！基金投研功能已成功实现")
print("="*70)

print("\n功能摘要:")
print("  - 侧边栏菜单: 基金投研（含概览、数据集合、基金分析） [OK]")
print("  - 前端路由: /funds (含3个子路由) [OK]")
print("  - 前端页面: index.vue, Collections.vue, FundAnalysis.vue [OK]")
print("  - 前端API: funds.ts [OK]")
print("  - 后端路由: funds.py [OK]")
print("  - 后端注册: main.py [OK]")

print("\n下一步:")
print("  1. 重启后端服务: python -m app.main")
print("  2. 启动前端服务: npm run dev")
print("  3. 访问应用并测试基金投研功能")
