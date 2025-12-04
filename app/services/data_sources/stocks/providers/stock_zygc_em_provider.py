"""
主营构成-东财数据提供者

东方财富网-个股-主营构成
接口: stock_zygc_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZygcEmProvider(BaseProvider):
    """主营构成-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_zygc_em"
    display_name = "主营构成-东财"
    akshare_func = "stock_zygc_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-个股-主营构成"
    collection_route = "/stocks/collections/stock_zygc_em"
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
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "报告日期", "type": "object", "description": "-"},
        {"name": "分类类型", "type": "object", "description": "-"},
        {"name": "主营构成", "type": "int64", "description": "-"},
        {"name": "主营收入", "type": "float64", "description": "注意单位: 元"},
        {"name": "收入比例", "type": "float64", "description": "-"},
        {"name": "主营成本", "type": "float64", "description": "注意单位: 元"},
        {"name": "成本比例", "type": "float64", "description": "-"},
        {"name": "主营利润", "type": "float64", "description": "注意单位: 元"},
        {"name": "利润比例", "type": "float64", "description": "-"},
        {"name": "毛利率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
