"""
分析stocks.py文件的collections部分
"""
from pathlib import Path
import re

stocks_file = Path(r'F:\source_code\TradingAgents-CN\app\routers\stocks.py')
content = stocks_file.read_text(encoding='utf-8')

print("="*80)
print("分析 stocks.py 文件")
print("="*80)

print(f"\n文件大小: {len(content)} 字符")
print(f"总字典数量 ({{): {content.count('{')}")

# 查找collections定义
match = re.search(r'collections\s*=\s*\[', content)
if match:
    print(f"\n找到 collections = [ 在位置 {match.start()}")
    
    # 手动匹配括号来找结束位置
    start_pos = match.end()
    bracket_count = 1
    current_pos = start_pos
    
    while current_pos < len(content) and bracket_count > 0:
        if content[current_pos] == '[':
            bracket_count += 1
        elif content[current_pos] == ']':
            bracket_count -= 1
        current_pos += 1
    
    end_pos = current_pos - 1
    
    collections_block = content[start_pos:end_pos]
    
    print(f"collections块大小: {len(collections_block)} 字符")
    name_double = collections_block.count('"name"')
    name_single = collections_block.count("'name'")
    print(f"collections中的项目数 (双引号name): {name_double}")
    print(f"collections中的项目数 (单引号name): {name_single}")
    
    # 显示前1000个字符
    print(f"\ncollections块的前1000个字符:")
    print(collections_block[:1000])
    
    # 显示后500个字符
    print(f"\ncollections块的最后500个字符:")
    print(collections_block[-500:])
else:
    print("\n错误: 找不到 collections = [")

# 查找是否有API路由
print(f"\n\nAPI路由检查:")
print(f"GET /collections/xxx: {content.count('@router.get(\"/collections/')}")
print(f"POST /collections/xxx/refresh: {content.count('@router.post(\"/collections/')}")
print(f"DELETE /collections/xxx/clear: {content.count('@router.delete(\"/collections/')}")
