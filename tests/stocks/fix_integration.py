"""
修复集合整合问题 - 正确提取和添加290个集合
"""
from pathlib import Path
import re

# 项目根目录
project_root = Path(__file__).parent.parent.parent
stocks_router_file = project_root / "app" / "routers" / "stocks.py"
backup_file = stocks_router_file.with_suffix('.py.backup')

print("="*80)
print("修复集合整合问题")
print("="*80)

# 先恢复备份
if backup_file.exists():
    print(f"\n1. 恢复原始备份文件...")
    content = backup_file.read_text(encoding='utf-8')
    print(f"   原文件大小: {len(content)} 字符")
else:
    print("错误: 找不到备份文件")
    exit(1)

# 读取生成的集合注册文件
collections_file = Path(__file__).parent / "generated_collections_registration.py"
collections_content = collections_file.read_text(encoding='utf-8')

# 使用简单的字符串分割来提取集合列表内容
# 找到 "collections = [" 之后和最后的 "]" 之前的所有内容
start_marker = "collections = ["
end_marker = "\n]"

start_idx = collections_content.find(start_marker)
if start_idx == -1:
    print("错误: 找不到 collections = [")
    exit(1)

start_idx += len(start_marker)
end_idx = collections_content.rfind(end_marker)
if end_idx == -1:
    print("错误: 找不到结束的 ]")
    exit(1)

collections_items = collections_content[start_idx:end_idx].strip()
print(f"\n2. 提取集合注册代码...")
print(f"   提取的内容大小: {len(collections_items)} 字符")
print(f"   集合数量: {collections_items.count('{name')} 个")

# 查找原文件中的 collections 列表
collections_pattern = r'(collections\s*=\s*\[)'
match = re.search(collections_pattern, content)

if not match:
    print("错误: 在原文件中找不到 collections 列表")
    exit(1)

# 找到 collections = [ 的位置
insert_pos = match.end()

# 找到对应的结束 ]
# 从 insert_pos 开始，手动匹配括号
bracket_count = 1
current_pos = insert_pos
in_string = False
escape_next = False

while current_pos < len(content) and bracket_count > 0:
    char = content[current_pos]
    
    if escape_next:
        escape_next = False
        current_pos += 1
        continue
    
    if char == '\\':
        escape_next = True
    elif char == '"' or char == "'":
        # 简化处理：忽略字符串内的括号
        in_string = not in_string
    elif not in_string:
        if char == '[':
            bracket_count += 1
        elif char == ']':
            bracket_count -= 1
    
    current_pos += 1

if bracket_count != 0:
    print("错误: 无法正确匹配 collections 列表的结束位置")
    exit(1)

end_pos = current_pos - 1  # 不包括最后的 ]

# 提取现有的集合内容
existing_content = content[insert_pos:end_pos].strip()
print(f"\n3. 分析现有集合...")
print(f"   现有内容大小: {len(existing_content)} 字符")
print(f"   现有集合数量: {existing_content.count('{name') if existing_content else 0} 个")

# 构建新的集合列表内容
if existing_content:
    # 确保现有内容以逗号结尾
    if not existing_content.rstrip().endswith(','):
        existing_content = existing_content.rstrip() + ','
    new_collections_content = f"\n{existing_content}\n{collections_items}\n"
else:
    new_collections_content = f"\n{collections_items}\n"

# 替换内容
new_content = content[:insert_pos] + new_collections_content + content[end_pos:]

print(f"\n4. 写入新文件...")
print(f"   新文件大小: {len(new_content)} 字符")
total_collections = new_content.count('"name":')
print(f"   总集合数量: {total_collections} 个")

# 保存新文件
stocks_router_file.write_text(new_content, encoding='utf-8')
print(f"   已保存: {stocks_router_file}")

print("\n" + "="*80)
print("修复完成！")
print("="*80)
print(f"\n现在 collections 列表应该包含约 {total_collections} 个集合")
print("\n请重启后端服务：")
print("  cd F:\\source_code\\TradingAgents-CN")
print("  uvicorn app.main:app --host 0.0.0.0 --port 8848 --reload")
print("="*80)
