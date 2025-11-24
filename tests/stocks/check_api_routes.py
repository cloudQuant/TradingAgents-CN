"""
检查API路由是否添加
"""
from pathlib import Path

stocks_file = Path(r'F:\source_code\TradingAgents-CN\app\routers\stocks.py')
content = stocks_file.read_text(encoding='utf-8')

print("="*80)
print("检查API路由")
print("="*80)

# 查找自动生成的API路由标记
marker = "# ========== 自动生成的API路由"
pos = content.find(marker)

if pos != -1:
    print(f"\n找到自动生成的API路由标记在位置 {pos}")
    api_section = content[pos:min(pos+3000, len(content))]
    print(f"\nAPI路由部分(前3000字符):")
    print(api_section)
else:
    print(f"\n未找到自动生成的API路由标记")
    print(f"\n文件最后2000个字符:")
    print(content[-2000:])

# 统计路由数量
print(f"\n\n路由统计:")
print(f"@router.get: {content.count('@router.get')}")
print(f"@router.post: {content.count('@router.post')}")
print(f"@router.delete: {content.count('@router.delete')}")
print(f"@router.put: {content.count('@router.put')}")
