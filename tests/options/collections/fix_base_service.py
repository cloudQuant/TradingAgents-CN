#!/usr/bin/env python
"""
修复 base_service.py 中的参数过滤问题
问题：frontend_only_params 错误地包含了业务参数如 symbol, year, date 等
"""

def fix_base_service():
    """修复 base_service.py"""
    file_path = "/Users/yunjinqi/Documents/TradingAgents-CN/app/services/data_sources/base_service.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复 _simple_batch_update 中的 frontend_only_params
    # 移除业务参数，只保留真正的前端参数
    old_text = '''        frontend_only_params = {
            'update_type', 'update_mode', 'batch_update', 'batch_size',
            'page', 'limit', 'skip', 'filters', 'sort', 'order',
            'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
            'force', 'clear_first', 'overwrite', 'mode', 'concurrency',
            # 可选业务参数（值为None时应过滤）
            'fund_code', 'symbol', 'year', 'date', 'period', 'adjust',
            'start_year', 'end_year', 'delay', 'code'
        }
        # 只保留非前端特有参数且值不为None的参数
        provider_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params and v is not None}'''
    
    new_text = '''        frontend_only_params = {
            'update_type', 'update_mode', 'batch_update', 'batch_size',
            'page', 'limit', 'skip', 'filters', 'sort', 'order',
            'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
            'force', 'clear_first', 'overwrite', 'mode', 'concurrency'
        }
        # 只保留非前端特有参数且值不为None的参数
        # 注意：业务参数如 symbol, year, date 等不应被过滤
        provider_kwargs = {k: v for k, v in kwargs.items() if k not in frontend_only_params and v is not None}'''
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        print("✓ 修复了 _simple_batch_update 中的 frontend_only_params")
    else:
        print("✗ 未找到需要修复的内容，可能已经修复或格式不同")
        # 尝试更宽松的匹配
        import re
        pattern = r"frontend_only_params = \{[^}]*'fund_code', 'symbol', 'year', 'date'[^}]*\}"
        if re.search(pattern, content):
            print("  发现包含业务参数的 frontend_only_params，尝试手动修复")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已保存到 {file_path}")


if __name__ == "__main__":
    fix_base_service()
