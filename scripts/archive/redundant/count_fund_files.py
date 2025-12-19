"""统计生成的fund provider和service文件数量"""
from pathlib import Path

project_root = Path(__file__).parent.parent
providers_dir = project_root / "app" / "services" / "data_sources" / "funds" / "providers"
services_dir = project_root / "app" / "services" / "data_sources" / "funds" / "services"

provider_files = list(providers_dir.glob("*.py"))
service_files = list(services_dir.glob("*.py"))

# 排除__init__.py
provider_files = [f for f in provider_files if f.name != "__init__.py"]
service_files = [f for f in service_files if f.name != "__init__.py"]

print(f"Provider文件数量: {len(provider_files)}")
print(f"Service文件数量: {len(service_files)}")
print(f"总计: {len(provider_files) + len(service_files)}")

print("\n所有Provider文件:")
for f in sorted(provider_files):
    print(f"  - {f.name}")
    
print(f"\n总共有 {len(provider_files)} 个数据集合")
