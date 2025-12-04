"""
龙虎榜-机构席位成交明细数据提供者

新浪财经-龙虎榜-机构席位成交明细
接口: stock_lhb_jgmx_sina
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockLhbJgmxSinaProvider(SimpleProvider):
    """龙虎榜-机构席位成交明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_jgmx_sina"
    display_name = "龙虎榜-机构席位成交明细"
    akshare_func = "stock_lhb_jgmx_sina"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "新浪财经-龙虎榜-机构席位成交明细"
    collection_route = "/stocks/collections/stock_lhb_jgmx_sina"
    collection_category = "龙虎榜"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "机构席位买入额", "type": "float64", "description": "注意单位: 万"},
        {"name": "机构席位卖出额", "type": "float64", "description": "注意单位: 万"},
        {"name": "类型", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
