"""
盈利预测-东方财富数据提供者

东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常
接口: stock_profit_forecast_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockProfitForecastEmProvider(BaseProvider):
    """盈利预测-东方财富数据提供者"""
    
    # 必填属性
    collection_name = "stock_profit_forecast_em"
    display_name = "盈利预测-东方财富"
    akshare_func = "stock_profit_forecast_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-研究报告-盈利预测; 该数据源网页端返回数据有异常, 本接口已修复该异常"
    collection_route = "/stocks/collections/stock_profit_forecast_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = []

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "研报数", "type": "int64", "description": "-"},
        {"name": "机构投资评级(近六个月)-买入", "type": "float64", "description": "-"},
        {"name": "机构投资评级(近六个月)-增持", "type": "float64", "description": "-"},
        {"name": "机构投资评级(近六个月)-中性", "type": "float64", "description": "-"},
        {"name": "机构投资评级(近六个月)-减持", "type": "int64", "description": "-"},
        {"name": "机构投资评级(近六个月)-卖出", "type": "int64", "description": "-"},
        {"name": "xxxx预测每股收益", "type": "float64", "description": "-"},
        {"name": "xxxx预测每股收益", "type": "float64", "description": "-"},
        {"name": "xxxx预测每股收益", "type": "float64", "description": "-"},
        {"name": "xxxx预测每股收益", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
