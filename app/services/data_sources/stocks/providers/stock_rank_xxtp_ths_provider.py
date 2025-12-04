"""
向下突破数据提供者

同花顺-数据中心-技术选股-向下突破
接口: stock_rank_xxtp_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockRankXxtpThsProvider(BaseProvider):
    """向下突破数据提供者"""
    
    # 必填属性
    collection_name = "stock_rank_xxtp_ths"
    display_name = "向下突破"
    akshare_func = "stock_rank_xxtp_ths"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "同花顺-数据中心-技术选股-向下突破"
    collection_route = "/stocks/collections/stock_rank_xxtp_ths"
    collection_category = "默认"

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
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 元"},
        {"name": "成交额", "type": "object", "description": "注意单位: 元"},
        {"name": "成交量", "type": "object", "description": "注意单位: 股"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
