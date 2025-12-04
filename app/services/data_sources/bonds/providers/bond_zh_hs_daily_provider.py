"""
沪深债券历史行情数据提供者（重构版：继承BaseProvider）

需求文档: tests/bonds/requirements/04_沪深债券历史行情.md
数据唯一标识: 债券代码和日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhHsDailyProvider(BaseProvider):
    """沪深债券历史行情数据提供者"""
    
    # 基本属性
    collection_name = "bond_zh_hs_daily"
    display_name = "沪深债券历史行情"
    akshare_func = "bond_zh_hs_daily"
    unique_keys = ["债券代码", "date"]  # 以债券代码和日期作为唯一标识
    
    # 参数映射
    param_mapping = {
        "bond_code": "symbol",
        "symbol": "symbol",
        "code": "symbol",
    }
    required_params = ["symbol"]
    add_param_columns = {"symbol": "债券代码"}
    
    # 元信息
    collection_description = "沪深债券历史行情数据（日线），支持按日期查询"
    collection_route = "/bonds/collections/bond_zh_hs_daily"
    collection_order = 4
    
    # 字段信息
    field_info = [
        {"name": "债券代码", "type": "string", "description": "债券代码"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
