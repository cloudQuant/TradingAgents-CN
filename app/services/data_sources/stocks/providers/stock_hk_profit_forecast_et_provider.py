"""
港股盈利预测-经济通数据提供者

经济通-公司资料-盈利预测
接口: stock_hk_profit_forecast_et
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkProfitForecastEtProvider(BaseProvider):
    """港股盈利预测-经济通数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_profit_forecast_et"
    display_name = "港股盈利预测-经济通"
    akshare_func = "stock_hk_profit_forecast_et"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "经济通-公司资料-盈利预测"
    collection_route = "/stocks/collections/stock_hk_profit_forecast_et"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "财政年度", "type": "object", "description": "-"},
        {"name": "纯利/亏损", "type": "float64", "description": "注意单位：百万元人民币/百万港元"},
        {"name": "每股盈利", "type": "float64", "description": "注意单位：分/港仙"},
        {"name": "每股派息", "type": "float64", "description": "注意单位：分/港仙"},
        {"name": "证券商", "type": "object", "description": "-"},
        {"name": "评级", "type": "object", "description": "-"},
        {"name": "目标价", "type": "float64", "description": "注意单位：港元"},
        {"name": "更新日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
