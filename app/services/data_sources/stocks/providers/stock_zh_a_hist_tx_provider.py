"""
历史行情数据-腾讯数据提供者

腾讯证券-日频-股票历史数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
接口: stock_zh_a_hist_tx
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAHistTxProvider(BaseProvider):
    """历史行情数据-腾讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_hist_tx"
    display_name = "历史行情数据-腾讯"
    akshare_func = "stock_zh_a_hist_tx"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "腾讯证券-日频-股票历史数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取"
    collection_route = "/stocks/collections/stock_zh_a_hist_tx"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "start_date": "start_date",
        "end_date": "end_date",
        "adjust": "adjust",
        "timeout": "timeout"
    }
    
    # 必填参数
    required_params = ['symbol', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "交易日"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "amount", "type": "int64", "description": "注意单位: 手"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
