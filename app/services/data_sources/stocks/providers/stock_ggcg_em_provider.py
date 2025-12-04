"""
股东增减持数据提供者

东方财富网-数据中心-特色数据-高管持股
接口: stock_ggcg_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGgcgEmProvider(BaseProvider):
    """股东增减持数据提供者"""
    
    # 必填属性
    collection_name = "stock_ggcg_em"
    display_name = "股东增减持"
    akshare_func = "stock_ggcg_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-高管持股"
    collection_route = "/stocks/collections/stock_ggcg_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "持股变动信息-增减", "type": "float64", "description": "-"},
        {"name": "持股变动信息-变动数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "持股变动信息-占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "持股变动信息-占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "变动后持股情况-持股总数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动后持股情况-占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "变动后持股情况-持流通股数", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动后持股情况-占流通股比例", "type": "float64", "description": "注意单位: %"},
        {"name": "变动开始日", "type": "object", "description": "-"},
        {"name": "变动截止日", "type": "object", "description": "-"},
        {"name": "公告日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
