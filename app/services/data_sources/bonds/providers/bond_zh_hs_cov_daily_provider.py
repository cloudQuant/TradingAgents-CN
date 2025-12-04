"""
可转债历史行情-日频数据提供者（重构版）

需求文档: tests/bonds/requirements/06_可转债历史行情-日频.md
数据唯一标识: 可转债代码和日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhHsCovDailyProvider(BaseProvider):
    """可转债历史行情-日频数据提供者"""
    
    collection_name = "bond_zh_hs_cov_daily"
    display_name = "可转债历史行情-日频"
    akshare_func = "bond_zh_hs_cov_daily"
    unique_keys = ["可转债代码", "date"]
    
    param_mapping = {"bond_code": "symbol", "symbol": "symbol", "code": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "可转债代码"}
    
    collection_description = "沪深可转债历史行情数据（日线）"
    collection_route = "/bonds/collections/bond_zh_hs_cov_daily"
    collection_order = 6
    
    field_info = [
        {"name": "可转债代码", "type": "string", "description": "可转债代码"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
