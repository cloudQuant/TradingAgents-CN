"""
REITs历史行情-东财数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class ReitsHistEmProvider(BaseProvider):
    """REITs历史行情-东财数据提供者（需要基金代码参数）"""

    collection_description = "东方财富网-行情中心-REITs-沪深 REITs-历史行情（需要基金代码，支持单个/批量更新）"
    collection_route = "/funds/collections/reits_hist_em"
    collection_order = 60

    collection_name = "reits_hist_em"
    display_name = "REITs历史行情-东财"
    akshare_func = "reits_hist_em"
    unique_keys = ["基金代码", "日期"]
    
    # 参数映射：symbol/fund_code/code 都映射到 symbol
    param_mapping = {
        "symbol": "symbol",
        "fund_code": "symbol",
        "code": "symbol",
    }
    required_params = ["symbol"]
    
    # 自动添加参数列：将symbol参数值写入"基金代码"列
    add_param_columns = {
        "symbol": "基金代码",
    }
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"

    field_info = [
        {"name": "基金代码", "type": "string", "description": "REITs代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "今开", "type": "float", "description": "今开价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "振幅", "type": "float", "description": "振幅（%）"},
        {"name": "换手", "type": "float", "description": "换手（%）"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: reits_hist_em"},
    ]
