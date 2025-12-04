"""
活跃 A 股统计数据提供者

东方财富网-数据中心-大宗交易-活跃 A 股统计
接口: stock_dzjy_hygtj
"""
from app.services.data_sources.base_provider import BaseProvider


class StockDzjyHygtjProvider(BaseProvider):
    """活跃 A 股统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_hygtj"
    display_name = "活跃 A 股统计"
    akshare_func = "stock_dzjy_hygtj"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-活跃 A 股统计"
    collection_route = "/stocks/collections/stock_dzjy_hygtj"
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
        {"name": "证券代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最近上榜日", "type": "object", "description": "-"},
        {"name": "上榜次数-总计", "type": "int64", "description": "-"},
        {"name": "上榜次数-溢价", "type": "int64", "description": "-"},
        {"name": "上榜次数-折价", "type": "int64", "description": "-"},
        {"name": "总成交额", "type": "float64", "description": "注意单位: 万元"},
        {"name": "折溢率", "type": "float64", "description": "注意单位: 万元"},
        {"name": "成交总额/流通市值", "type": "float64", "description": "-"},
        {"name": "上榜日后平均涨跌幅-1日", "type": "float64", "description": "注意符号: %"},
        {"name": "上榜日后平均涨跌幅-5日", "type": "float64", "description": "注意符号: %"},
        {"name": "上榜日后平均涨跌幅-10日", "type": "float64", "description": "注意符号: %"},
        {"name": "上榜日后平均涨跌幅-20日", "type": "float64", "description": "注意符号: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
