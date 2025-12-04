"""
一致行动人数据提供者

东方财富网-数据中心-特色数据-一致行动人
接口: stock_yzxdr_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockYzxdrEmProvider(BaseProvider):
    """一致行动人数据提供者"""
    
    # 必填属性
    collection_name = "stock_yzxdr_em"
    display_name = "一致行动人"
    akshare_func = "stock_yzxdr_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-一致行动人"
    collection_route = "/stocks/collections/stock_yzxdr_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "一致行动人", "type": "object", "description": "-"},
        {"name": "股东排名", "type": "object", "description": "-"},
        {"name": "持股数量", "type": "int64", "description": "-"},
        {"name": "持股比例", "type": "float64", "description": "-"},
        {"name": "持股数量变动", "type": "object", "description": "注意单位: %"},
        {"name": "行业", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
