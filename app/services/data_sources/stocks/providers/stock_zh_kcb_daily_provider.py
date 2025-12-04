"""
历史行情数据数据提供者

新浪财经-科创板股票历史行情数据
接口: stock_zh_kcb_daily
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhKcbDailyProvider(BaseProvider):
    """历史行情数据数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_kcb_daily"
    display_name = "历史行情数据"
    akshare_func = "stock_zh_kcb_daily"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-科创板股票历史行情数据"
    collection_route = "/stocks/collections/stock_zh_kcb_daily"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "-"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "high", "type": "float64", "description": "最高价"},
        {"name": "low", "type": "float64", "description": "最低价"},
        {"name": "open", "type": "float64", "description": "开盘价"},
        {"name": "volume", "type": "float64", "description": "成交量(股)"},
        {"name": "after_volume", "type": "float64", "description": "盘后量; 参见[科创板盘后固定价格交易](http://www.sse.com.cn/lawandrules/sserules/tib/trading/c/4729491.shtml)"},
        {"name": "after_amount", "type": "float64", "description": "盘后额; 参见[科创板盘后固定价格交易](http://www.sse.com.cn/lawandrules/sserules/tib/trading/c/4729491.shtml)"},
        {"name": "outstanding_share", "type": "float64", "description": "流通股本(股)"},
        {"name": "turnover", "type": "float64", "description": "换手率=成交量(股)/流通股本(股)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
