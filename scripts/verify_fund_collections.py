"""验证fund_refresh_service.py中的handlers和生成的文件是否匹配"""
import re
from pathlib import Path

# 读取fund_refresh_service.py中的handlers
fund_refresh_file = Path("app/services/fund_refresh_service.py")
content = fund_refresh_file.read_text(encoding='utf-8')

# 提取handlers中的所有collection名称
pattern = r'"([a-z_]+)":\s*self\._refresh_'
handlers_collections = re.findall(pattern, content)

print(f"fund_refresh_service.py中的handlers数量: {len(handlers_collections)}")
print("\nHandlers中的所有集合:")
for i, name in enumerate(handlers_collections, 1):
    print(f"{i:2d}. {name}")

# 读取生成脚本中的FUND_COLLECTIONS
generate_script = Path("scripts/generate_fund_modules.py")
script_content = generate_script.read_text(encoding='utf-8')

# 提取FUND_COLLECTIONS字典中的键
pattern2 = r'"([a-z_]+)":\s*\{'
collections_in_script = re.findall(pattern2, script_content)

print(f"\n\n生成脚本中的FUND_COLLECTIONS数量: {len(collections_in_script)}")

# 检查哪些在handlers中但不在生成脚本中
missing_in_script = set(handlers_collections) - set(collections_in_script)
if missing_in_script:
    print(f"\n❌ 在handlers中但不在生成脚本中的集合 ({len(missing_in_script)}个):")
    for name in sorted(missing_in_script):
        print(f"  - {name}")

# 检查哪些在生成脚本中但不在handlers中
extra_in_script = set(collections_in_script) - set(handlers_collections)
if extra_in_script:
    print(f"\n⚠️  在生成脚本中但不在handlers中的集合 ({len(extra_in_script)}个):")
    for name in sorted(extra_in_script):
        print(f"  - {name}")

# 检查重复
from collections import Counter
duplicates_in_script = [name for name, count in Counter(collections_in_script).items() if count > 1]
if duplicates_in_script:
    print(f"\n⚠️  生成脚本中的重复集合:")
    for name in duplicates_in_script:
        print(f"  - {name} (出现{Counter(collections_in_script)[name]}次)")

print(f"\n\n✅ 匹配的集合数量: {len(set(handlers_collections) & set(collections_in_script))}")
