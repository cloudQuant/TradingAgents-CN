"""
检查collections文件内容
"""
from pathlib import Path

# 读取生成的collections文件
collections_file = Path(__file__).parent / "generated_collections_registration.py"
content = collections_file.read_text(encoding='utf-8')

# 提取collections列表
start = content.find('collections = [')
end = content.rfind('\n]')

if start == -1 or end == -1:
    print("错误: 找不到collections列表")
    exit(1)

start += len('collections = [')
collections_content = content[start:end].strip()

print(f"Collections内容大小: {len(collections_content)} 字符")
print(f"字典数量 ({{): {collections_content.count('{')}")
print(f"name字段数量: {collections_content.count('\"name\"')}")
print(f"\n前1000个字符:")
print(collections_content[:1000])
print("\n...")
print(f"\n最后500个字符:")
print(collections_content[-500:])
