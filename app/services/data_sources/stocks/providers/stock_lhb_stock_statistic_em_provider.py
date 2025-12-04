"""
个股上榜统计数据提供者

东方财富网-数据中心-龙虎榜单-个股上榜统计
接口: stock_lhb_stock_statistic_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockLhbStockStatisticEmProvider(BaseProvider):
    """个股上榜统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_lhb_stock_statistic_em"
    display_name = "个股上榜统计"
    akshare_func = "stock_lhb_stock_statistic_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-龙虎榜单-个股上榜统计"
    collection_route = "/stocks/collections/stock_lhb_stock_statistic_em"
    collection_category = "龙虎榜"

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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最近上榜日", "type": "object", "description": "-"},
        {"name": "收盘价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "上榜次数", "type": "int64", "description": "-"},
        {"name": "龙虎榜净买额", "type": "float64", "description": "-"},
        {"name": "龙虎榜买入额", "type": "float64", "description": "-"},
        {"name": "龙虎榜卖出额", "type": "float64", "description": "-"},
        {"name": "龙虎榜总成交额", "type": "float64", "description": "-"},
        {"name": "买方机构次数", "type": "int64", "description": "-"},
        {"name": "卖方机构次数", "type": "int64", "description": "-"},
        {"name": "机构买入净额", "type": "float64", "description": "-"},
        {"name": "机构买入总额", "type": "float64", "description": "-"},
        {"name": "机构卖出总额", "type": "float64", "description": "-"},
        {"name": "近1个月涨跌幅", "type": "float64", "description": "-"},
        {"name": "近3个月涨跌幅", "type": "float64", "description": "-"},
        {"name": "近6个月涨跌幅", "type": "float64", "description": "-"},
        {"name": "近1年涨跌幅", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
