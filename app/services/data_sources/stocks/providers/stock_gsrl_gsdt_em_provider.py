"""
公司动态数据提供者

东方财富网-数据中心-股市日历-公司动态
接口: stock_gsrl_gsdt_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockGsrlGsdtEmProvider(BaseProvider):
    """公司动态数据提供者"""
    
    # 必填属性
    collection_name = "stock_gsrl_gsdt_em"
    display_name = "公司动态"
    akshare_func = "stock_gsrl_gsdt_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-股市日历-公司动态"
    collection_route = "/stocks/collections/stock_gsrl_gsdt_em"
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
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "简称", "type": "object", "description": "-"},
        {"name": "事件类型", "type": "object", "description": "-"},
        {"name": "具体事项", "type": "object", "description": "-"},
        {"name": "交易日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
