"""
历史行情数据-新浪数据提供者

新浪财经-沪深京 A 股的数据, 历史数据按日频率更新; 注意其中的 **sh689009** 为 CDR, 请 通过 **ak.stock_zh_a_cdr_daily** 接口获取
接口: stock_zh_a_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhADailyProvider(BaseProvider):
    """历史行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_daily"
    display_name = "历史行情数据-新浪"
    akshare_func = "stock_zh_a_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-沪深京 A 股的数据, 历史数据按日频率更新; 注意其中的 **sh689009** 为 CDR, 请 通过 **ak.stock_zh_a_cdr_daily** 接口获取"
    collection_route = "/stocks/collections/stock_zh_a_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "volume", "type": "float64", "description": "成交量; 注意单位: 股"},
        {"name": "amount", "type": "float64", "description": "成交额; 注意单位: 元"},
        {"name": "outstanding_share", "type": "float64", "description": "流动股本; 注意单位: 股"},
        {"name": "turnover", "type": "float64", "description": "换手率=成交量/流动股本"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
