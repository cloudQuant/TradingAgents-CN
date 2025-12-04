"""
基金持股数据提供者

东方财富网-数据中心-主力数据-基金持仓
接口: stock_report_fund_hold
"""
from app.services.data_sources.base_provider import BaseProvider


class StockReportFundHoldProvider(BaseProvider):
    """基金持股数据提供者"""
    
    # 必填属性
    collection_name = "stock_report_fund_hold"
    display_name = "基金持股"
    akshare_func = "stock_report_fund_hold"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-主力数据-基金持仓"
    collection_route = "/stocks/collections/stock_report_fund_hold"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "持有基金家数", "type": "int64", "description": "注意单位: 家"},
        {"name": "持股总数", "type": "int64", "description": "注意单位: 股"},
        {"name": "持股市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "持股变化", "type": "object", "description": "-"},
        {"name": "持股变动数值", "type": "int64", "description": "注意单位: 股"},
        {"name": "持股变动比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
