"""
预约披露时间-东方财富数据提供者

东方财富-数据中心-年报季报-预约披露时间
接口: stock_yysj_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockYysjEmProvider(BaseProvider):
    """预约披露时间-东方财富数据提供者"""
    
    # 必填属性
    collection_name = "stock_yysj_em"
    display_name = "预约披露时间-东方财富"
    akshare_func = "stock_yysj_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-数据中心-年报季报-预约披露时间"
    collection_route = "/stocks/collections/stock_yysj_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "首次预约时间", "type": "object", "description": "-"},
        {"name": "一次变更日期", "type": "object", "description": "-"},
        {"name": "二次变更日期", "type": "object", "description": "-"},
        {"name": "三次变更日期", "type": "object", "description": "-"},
        {"name": "实际披露时间", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
