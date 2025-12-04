"""
IPO 受益股数据提供者

同花顺-数据中心-新股数据-IPO受益股
接口: stock_ipo_benefit_ths
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockIpoBenefitThsProvider(SimpleProvider):
    """IPO 受益股数据提供者"""
    
    # 必填属性
    collection_name = "stock_ipo_benefit_ths"
    display_name = "IPO 受益股"
    akshare_func = "stock_ipo_benefit_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-新股数据-IPO受益股"
    collection_route = "/stocks/collections/stock_ipo_benefit_ths"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "市值", "type": "object", "description": "注意单位: 元"},
        {"name": "参股家数", "type": "int64", "description": "-"},
        {"name": "投资总额", "type": "object", "description": "注意单位: 元"},
        {"name": "投资占市值比", "type": "float64", "description": "注意单位: %"},
        {"name": "参股对象", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
