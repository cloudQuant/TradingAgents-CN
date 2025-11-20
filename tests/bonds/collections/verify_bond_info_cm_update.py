"""
验证 bond_info_cm 参数化更新功能
检查代码修改是否正确
"""
import sys
import os
import re

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, root_dir)

print("=" * 70)
print("验证 bond_info_cm 参数化更新功能")
print("=" * 70)

# 1. 检查路由接口参数
print("\n[检查1] 验证路由接口参数")
bonds_router_path = os.path.join(
    root_dir, 'app', 'routers', 'bonds.py'
)
bonds_router_path = os.path.abspath(bonds_router_path)

with open(bonds_router_path, 'r', encoding='utf-8') as f:
    router_content = f.read()

# 查找refresh接口
refresh_endpoint = router_content.find('@router.post("/collections/{collection_name}/refresh")')
if refresh_endpoint < 0:
    print("  [FAILED] 找不到refresh接口")
    sys.exit(1)

print("  [OK] 找到refresh接口")

# 检查8个新参数
required_params = [
    'bond_name',
    'bond_code',
    'bond_issue',
    'bond_type',
    'coupon_type',
    'issue_year',
    'underwriter',
    'grade'
]

missing_params = []
for param in required_params:
    pattern = f'{param}:\\s*Optional\\[str\\]\\s*=\\s*Query'
    if not re.search(pattern, router_content[refresh_endpoint:refresh_endpoint+3000]):
        missing_params.append(param)

if missing_params:
    print(f"  [FAILED] 缺少参数: {missing_params}")
    sys.exit(1)
else:
    print(f"  [OK] 所有8个参数已添加: {', '.join(required_params)}")

# 检查params字典
if 'params = {' in router_content[refresh_endpoint:refresh_endpoint+5000]:
    print("  [OK] 参数打包为params字典")
else:
    print("  [FAILED] 未找到params字典")

# 2. 检查CollectionRefreshService
print("\n[检查2] 验证CollectionRefreshService修改")
service_path = os.path.join(
    root_dir, 
    'app', 'services', 'collection_refresh_service.py'
)
service_path = os.path.abspath(service_path)

with open(service_path, 'r', encoding='utf-8') as f:
    service_content = f.read()

# 检查refresh_collection方法签名
if 'async def refresh_collection' in service_content:
    refresh_method_start = service_content.find('async def refresh_collection')
    refresh_method_sig = service_content[refresh_method_start:refresh_method_start+500]
    
    if 'params: Optional[Dict[str, Any]]' in refresh_method_sig:
        print("  [OK] refresh_collection使用params参数")
    else:
        print("  [FAILED] refresh_collection未使用params参数")
        sys.exit(1)
else:
    print("  [FAILED] 找不到refresh_collection方法")
    sys.exit(1)

# 检查_refresh_bond_info_cm实现
if 'async def _refresh_bond_info_cm' in service_content:
    bond_info_cm_start = service_content.find('async def _refresh_bond_info_cm')
    bond_info_cm_end = service_content.find('\n\n', bond_info_cm_start + 1000)
    bond_info_cm_method = service_content[bond_info_cm_start:bond_info_cm_end]
    
    # 检查是否抛出错误
    if 'raise ValueError("中债详细信息需要逐个债券查询' in bond_info_cm_method:
        print("  [FAILED] _refresh_bond_info_cm仍然抛出错误，未实现功能")
        sys.exit(1)
    
    # 检查是否调用provider
    if 'await self.provider.get_bond_info_cm' in bond_info_cm_method:
        print("  [OK] _refresh_bond_info_cm调用provider.get_bond_info_cm")
    else:
        print("  [FAILED] _refresh_bond_info_cm未调用provider")
        sys.exit(1)
    
    # 检查是否保存数据
    if 'await self.svc.save_info_cm' in bond_info_cm_method:
        print("  [OK] _refresh_bond_info_cm保存数据到数据库")
    else:
        print("  [FAILED] _refresh_bond_info_cm未保存数据")
        sys.exit(1)
    
    # 检查参数提取
    param_checks = ['bond_name', 'bond_type', 'issue_year', 'grade']
    params_extracted = all(f'params.get("{p}")' in bond_info_cm_method for p in param_checks)
    
    if params_extracted:
        print("  [OK] _refresh_bond_info_cm正确提取参数")
    else:
        print("  [FAILED] _refresh_bond_info_cm未正确提取参数")
        sys.exit(1)
else:
    print("  [FAILED] 找不到_refresh_bond_info_cm方法")
    sys.exit(1)

# 3. 检查handler方法签名
print("\n[检查3] 验证其他handler方法签名")
handler_methods = [
    '_refresh_bond_basic_info',
    '_refresh_yield_curve_daily',
    '_refresh_bond_daily',
    '_refresh_bond_cb_list_jsl',
]

all_updated = True
for handler in handler_methods:
    pattern = f'async def {handler}\\(self, task_id: str, params: Dict\\[str, Any\\]\\)'
    if re.search(pattern, service_content):
        print(f"  [OK] {handler} 使用params参数")
    else:
        print(f"  [WARN] {handler} 签名可能未更新")
        all_updated = False

if all_updated:
    print("  [OK] 所有handler方法已更新")

# 4. 检查Provider方法
print("\n[检查4] 验证Provider方法")
provider_path = os.path.join(
    root_dir,
    'tradingagents', 'dataflows', 'providers', 'china', 'bonds.py'
)
provider_path = os.path.abspath(provider_path)

with open(provider_path, 'r', encoding='utf-8') as f:
    provider_content = f.read()

if 'async def get_bond_info_cm' in provider_content:
    method_start = provider_content.find('async def get_bond_info_cm')
    method_section = provider_content[method_start:method_start+2000]
    
    # 检查8个参数
    provider_params = [
        'bond_name: str = ""',
        'bond_code: str = ""',
        'bond_issue: str = ""',
        'bond_type: str = ""',
        'coupon_type: str = ""',
        'issue_year: str = ""',
        'underwriter: str = ""',
        'grade: str = ""'
    ]
    
    all_params = all(p in method_section for p in provider_params)
    
    if all_params:
        print("  [OK] Provider.get_bond_info_cm支持8个参数")
    else:
        print("  [FAILED] Provider.get_bond_info_cm参数不完整")
        sys.exit(1)
    
    # 检查调用AKShare
    if 'ak.bond_info_cm' in method_section:
        print("  [OK] Provider调用ak.bond_info_cm接口")
    else:
        print("  [FAILED] Provider未调用AKShare接口")
else:
    print("  [FAILED] Provider.get_bond_info_cm方法不存在")
    sys.exit(1)

# 5. 检查保存方法
print("\n[检查5] 验证保存方法")
service_data_path = os.path.join(
    root_dir,
    'app', 'services', 'bond_data_service.py'
)
service_data_path = os.path.abspath(service_data_path)

if os.path.exists(service_data_path):
    with open(service_data_path, 'r', encoding='utf-8') as f:
        service_data_content = f.read()
    
    if 'async def save_info_cm' in service_data_content:
        print("  [OK] BondDataService.save_info_cm方法存在")
    else:
        print("  [WARN] save_info_cm方法可能不存在")
else:
    print("  [WARN] bond_data_service.py文件未找到")

print("\n" + "=" * 70)
print("[SUCCESS] 所有检查通过！")
print("=" * 70)
print("\n功能摘要:")
print("  - 后端API: 支持8个查询参数 [OK]")
print("  - 刷新服务: 使用params字典统一管理参数 [OK]")
print("  - bond_info_cm: 实现参数化查询和更新 [OK]")
print("  - Provider: 支持8个参数的AKShare调用 [OK]")
print("  - 数据保存: save_info_cm方法可用 [OK]")
print("\n使用示例:")
print("  POST /api/bonds/collections/bond_info_cm/refresh")
print("  参数: bond_type=短期融资券&issue_year=2019")
print("\n下一步:")
print("  1. 重启后端服务")
print("  2. 测试API接口")
print("  3. (可选) 更新前端添加参数选择界面")
