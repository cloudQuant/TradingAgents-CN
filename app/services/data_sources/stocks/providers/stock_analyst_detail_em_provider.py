"""
分析师详情数据提供者

东方财富网-数据中心-研究报告-东方财富分析师指数-分析师详情
接口: stock_analyst_detail_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockAnalystDetailEmProvider(BaseProvider):
    """分析师详情数据提供者"""
    
    # 必填属性
    collection_name = "stock_analyst_detail_em"
    display_name = "分析师详情"
    akshare_func = "stock_analyst_detail_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-研究报告-东方财富分析师指数-分析师详情"
    collection_route = "/stocks/collections/stock_analyst_detail_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "analyst_id": "analyst_id",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['analyst_id', 'indicator']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "调入日期", "type": "object", "description": "-"},
        {"name": "最新评级日期", "type": "object", "description": "-"},
        {"name": "成交价格(前复权)", "type": "float64", "description": "-"},
        {"name": "最新价格", "type": "float64", "description": "-"},
        {"name": "阶段涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "调入日期", "type": "object", "description": "-"},
        {"name": "调出日期", "type": "object", "description": "-"},
        {"name": "调出原因", "type": "object", "description": "-"},
        {"name": "累计涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "value", "type": "float64", "description": "指数数值; 注意: 此指数为东方财富制定"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
