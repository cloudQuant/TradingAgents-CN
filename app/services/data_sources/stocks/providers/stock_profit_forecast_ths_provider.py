"""
盈利预测-同花顺数据提供者

同花顺-盈利预测
接口: stock_profit_forecast_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockProfitForecastThsProvider(BaseProvider):
    """盈利预测-同花顺数据提供者"""
    
    # 必填属性
    collection_name = "stock_profit_forecast_ths"
    display_name = "盈利预测-同花顺"
    akshare_func = "stock_profit_forecast_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-盈利预测"
    collection_route = "/stocks/collections/stock_profit_forecast_ths"
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
        {"name": "年度", "type": "object", "description": "-"},
        {"name": "预测机构数", "type": "int64", "description": "-"},
        {"name": "最小值", "type": "float64", "description": "-"},
        {"name": "均值", "type": "float64", "description": "-"},
        {"name": "最大值", "type": "float64", "description": "-"},
        {"name": "行业平均数", "type": "float64", "description": "-"},
        {"name": "年度", "type": "object", "description": "-"},
        {"name": "预测机构数", "type": "int64", "description": "-"},
        {"name": "最小值", "type": "float64", "description": "-"},
        {"name": "均值", "type": "float64", "description": "-"},
        {"name": "最大值", "type": "float64", "description": "-"},
        {"name": "行业平均数", "type": "float64", "description": "-"},
        {"name": "研究员", "type": "object", "description": "-"},
        {"name": "预测年报每股收益2022预测", "type": "float64", "description": "-"},
        {"name": "预测年报每股收益2023预测", "type": "float64", "description": "-"},
        {"name": "预测年报每股收益2024预测", "type": "float64", "description": "-"},
        {"name": "预测年报净利润2022预测", "type": "object", "description": "-"},
        {"name": "预测年报净利润2023预测", "type": "object", "description": "-"},
        {"name": "预测年报净利润2024预测", "type": "object", "description": "-"},
        {"name": "报告日期", "type": "object", "description": "-"},
        {"name": "预测指标", "type": "object", "description": "-"},
        {"name": "2019-实际值", "type": "object", "description": "-"},
        {"name": "2020-实际值", "type": "object", "description": "-"},
        {"name": "2021-实际值", "type": "object", "description": "-"},
        {"name": "预测2022-平均", "type": "object", "description": "-"},
        {"name": "预测2023-平均", "type": "object", "description": "-"},
        {"name": "预测2024-平均", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
