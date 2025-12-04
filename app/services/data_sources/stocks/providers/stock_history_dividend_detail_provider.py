"""
分红配股数据提供者

新浪财经-发行与分配-分红配股
接口: stock_history_dividend_detail
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHistoryDividendDetailProvider(BaseProvider):
    """分红配股数据提供者"""
    
    # 必填属性
    collection_name = "stock_history_dividend_detail"
    display_name = "分红配股"
    akshare_func = "stock_history_dividend_detail"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-发行与分配-分红配股"
    collection_route = "/stocks/collections/stock_history_dividend_detail"
    collection_category = "历史行情"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator', 'date']

    # 字段信息
    field_info = [
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "送股", "type": "int64", "description": "注意单位: 股"},
        {"name": "转增", "type": "int64", "description": "注意单位: 股"},
        {"name": "派息", "type": "float64", "description": "注意单位: 元; 税前"},
        {"name": "进度", "type": "object", "description": "-"},
        {"name": "除权除息日", "type": "object", "description": "-"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "红股上市日", "type": "object", "description": "-"},
        {"name": "item", "type": "object", "description": "所列项目"},
        {"name": "value", "type": "object", "description": "项目值"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "配股方案", "type": "float64", "description": "注意单位: 每10股配股股数"},
        {"name": "配股价格", "type": "float64", "description": "注意单位: 元"},
        {"name": "基准股本", "type": "int64", "description": "注意单位: 股"},
        {"name": "除权日", "type": "object", "description": "-"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "缴款起始日", "type": "object", "description": "-"},
        {"name": "缴款终止日", "type": "object", "description": "-"},
        {"name": "配股上市日", "type": "object", "description": "-"},
        {"name": "募集资金合计", "type": "float64", "description": "注意单位: 元"},
        {"name": "item", "type": "object", "description": "所列项目"},
        {"name": "value", "type": "object", "description": "项目值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
