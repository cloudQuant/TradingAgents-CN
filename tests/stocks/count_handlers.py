import re

with open('F:/source_code/TradingAgents-CN/app/services/stock_refresh_service.py', encoding='utf-8') as f:
    content = f.read()

handlers = re.findall(r'"(stock_[^"]+)":\s*self\._refresh_', content)
print(f'原有 handlers 数量: {len(handlers)}')
print('前 20 个:')
for h in handlers[:20]:
    print(f'  - {h}')
