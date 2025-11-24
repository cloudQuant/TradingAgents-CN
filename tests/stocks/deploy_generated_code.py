"""
将生成的代码部署到项目的正确位置
"""
import shutil
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent.parent
generated_code_dir = Path(__file__).parent / "generated_code"

# 目标目录
backend_providers_dir = project_root / "app" / "services" / "stock" / "providers"
backend_services_dir = project_root / "app" / "services" / "stock"
frontend_views_dir = project_root / "frontend" / "src" / "views" / "Stocks" / "Collections"

# 确保目标目录存在
backend_providers_dir.mkdir(parents=True, exist_ok=True)
backend_services_dir.mkdir(parents=True, exist_ok=True)
frontend_views_dir.mkdir(parents=True, exist_ok=True)

# 收集所有路由和集合注册代码
all_api_routes = []
all_collection_registrations = []
all_route_configs = []

# 遍历所有生成的集合
collection_dirs = sorted(generated_code_dir.iterdir())
print(f"找到 {len(collection_dirs)} 个集合要部署\n")

for idx, collection_dir in enumerate(collection_dirs, 1):
    if not collection_dir.is_dir():
        continue
    
    collection_name = collection_dir.name
    print(f"[{idx}/{len(collection_dirs)}] 部署 {collection_name}...")
    
    try:
        # 1. 复制 Provider
        provider_src = collection_dir / "provider.py"
        provider_dst = backend_providers_dir / f"{collection_name}_provider.py"
        if provider_src.exists():
            shutil.copy2(provider_src, provider_dst)
            print(f"  [+] Provider: {provider_dst.relative_to(project_root)}")
        
        # 2. 复制 Service
        service_src = collection_dir / "service.py"
        service_dst = backend_services_dir / f"{collection_name}_service.py"
        if service_src.exists():
            shutil.copy2(service_src, service_dst)
            print(f"  [+] Service: {service_dst.relative_to(project_root)}")
        
        # 3. 收集 API 路由代码
        api_routes_src = collection_dir / "api_routes.py"
        if api_routes_src.exists():
            all_api_routes.append(api_routes_src.read_text(encoding='utf-8'))
        
        # 4. 复制 Vue 组件
        component_src = collection_dir / "component.vue"
        # 将下划线转为驼峰命名
        component_name = ''.join(word.title() for word in collection_name.split('_'))
        component_dst = frontend_views_dir / f"{component_name}.vue"
        if component_src.exists():
            shutil.copy2(component_src, component_dst)
            print(f"  [+] Component: {component_dst.relative_to(project_root)}")
        
        # 5. 收集路由配置
        route_config_src = collection_dir / "route_config.ts"
        if route_config_src.exists():
            all_route_configs.append(route_config_src.read_text(encoding='utf-8'))
        
        # 6. 收集集合注册代码
        collection_reg_src = collection_dir / "collection_registration.py"
        if collection_reg_src.exists():
            all_collection_registrations.append(collection_reg_src.read_text(encoding='utf-8'))
        
    except Exception as e:
        print(f"  [x] Error: {e}")

# 生成汇总文件
print("\n生成汇总文件...")

# API 路由汇总文件
api_routes_file = project_root / "tests" / "stocks" / "generated_api_routes.py"
api_routes_content = '''"""
生成的API路由代码
需要手动添加到 app/routers/stocks.py 文件中
"""

# 将以下代码添加到 app/routers/stocks.py 的路由定义中
# 注意: 需要先导入必要的依赖

''' + '\n\n'.join(all_api_routes)
api_routes_file.write_text(api_routes_content, encoding='utf-8')
print(f"[+] API routes: {api_routes_file.relative_to(project_root)}")

# 集合注册汇总文件
collections_file = project_root / "tests" / "stocks" / "generated_collections_registration.py"
collections_content = '''"""
生成的集合注册代码
需要手动添加到 app/routers/stocks.py 的 collections 列表中
"""

# 将以下代码添加到 collections 列表中
collections = [
''' + '\n'.join(all_collection_registrations) + '''
]
'''
collections_file.write_text(collections_content, encoding='utf-8')
print(f"[+] Collections registration: {collections_file.relative_to(project_root)}")

# 前端路由配置汇总文件
routes_file = project_root / "tests" / "stocks" / "generated_routes_config.ts"
routes_content = '''/**
 * 生成的前端路由配置
 * 需要手动添加到 frontend/src/router/index.ts 文件中
 */

// 将以下路由配置添加到路由数组中
const generatedRoutes = [
''' + '\n'.join(all_route_configs) + '''
]

export default generatedRoutes
'''
routes_file.write_text(routes_content, encoding='utf-8')
print(f"[+] Frontend routes: {routes_file.relative_to(project_root)}")

print("\n" + "=" * 80)
print("部署完成！")
print("=" * 80)
print("\n后续步骤:")
print("1. 将 generated_api_routes.py 中的代码添加到 app/routers/stocks.py")
print("2. 将 generated_collections_registration.py 中的代码添加到 app/routers/stocks.py 的 collections 列表")
print("3. 将 generated_routes_config.ts 中的路由配置添加到 frontend/src/router/index.ts")
print("4. 重启后端和前端服务")
print("5. 运行测试验证")
print("=" * 80)
