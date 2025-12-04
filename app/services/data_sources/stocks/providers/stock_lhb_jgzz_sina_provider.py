"""
龙虎榜-机构席位追踪数据提供者

新浪财经-龙虎榜-机构席位追踪
接口: stock_lhb_jgzz_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbJgzzSinaProvider(BaseProvider):
    """龙虎榜-机构席位追踪数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_jgzz_sina"
    display_name = "龙虎榜-机构席位追踪"
    akshare_func = "stock_lhb_jgzz_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-龙虎榜-机构席位追踪"
    collection_route = "/stocks/collections/stock_lhb_jgzz_sina"
    collection_category = "龙虎榜"

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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "累积买入额", "type": "float64", "description": "注意单位: 万"},
        {"name": "买入次数", "type": "float64", "description": "-"},
        {"name": "累积卖出额", "type": "float64", "description": "注意单位: 万"},
        {"name": "卖出次数", "type": "float64", "description": "-"},
        {"name": "净额", "type": "float64", "description": "注意单位: 万"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
