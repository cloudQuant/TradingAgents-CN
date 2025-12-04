"""
历史行情数据-东财数据提供者

东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
接口: stock_zh_a_hist
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAHistProvider(BaseProvider):
    """历史行情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_hist"
    display_name = "历史行情数据-东财"
    akshare_func = "stock_zh_a_hist"
    unique_keys = ['股票代码', '日期']
    
    # 可选属性
    collection_description = "东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取"
    collection_route = "/stocks/collections/stock_zh_a_hist"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "period": "period",
        "start_date": "start_date",
        "end_date": "end_date",
        "adjust": "adjust",
        "timeout": "timeout"
    }
    
    # 必填参数
    required_params = ['symbol', 'period', 'start_date', 'end_date']

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "交易日"},
        {"name": "股票代码", "type": "object", "description": "不带市场标识的股票代码"},
        {"name": "开盘", "type": "float64", "description": "开盘价"},
        {"name": "收盘", "type": "float64", "description": "收盘价"},
        {"name": "最高", "type": "float64", "description": "最高价"},
        {"name": "最低", "type": "float64", "description": "最低价"},
        {"name": "成交量", "type": "int64", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 元"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
