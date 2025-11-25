"""测试参数过滤逻辑"""
import sys
sys.path.insert(0, '.')

# 模拟参数过滤
FRONTEND_ONLY_PARAMS = {
    'batch', 'page', 'limit', 'skip', 'filters', 'sort', 'order',
    'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
    'force', 'clear_first', 'overwrite'
}

# 测试参数
test_params = {'batch': True, 'symbol': '000001', 'year': '2023'}

api_params = {}
if test_params:
    api_params = {
        k: v for k, v in test_params.items() 
        if k not in FRONTEND_ONLY_PARAMS
    }

print(f"原始参数: {test_params}")
print(f"过滤后参数: {api_params}")
print(f"batch 是否被过滤: {'batch' not in api_params}")
