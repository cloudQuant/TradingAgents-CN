"""
个股商誉减值明细数据提供者

东方财富网-数据中心-特色数据-商誉-个股商誉减值明细
接口: stock_sy_jz_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSyJzEmProvider(BaseProvider):
    """个股商誉减值明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_sy_jz_em"
    display_name = "个股商誉减值明细"
    akshare_func = "stock_sy_jz_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-商誉-个股商誉减值明细"
    collection_route = "/stocks/collections/stock_sy_jz_em"
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
        {"name": "商誉", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉减值", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉减值占净资产比例", "type": "float64", "description": "-"},
        {"name": "净利润", "type": "float64", "description": "注意单位: 元"},
        {"name": "商誉减值占净利润比例", "type": "float64", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "交易市场", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
