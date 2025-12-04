"""
行业商誉数据提供者

东方财富网-数据中心-特色数据-商誉-行业商誉
接口: stock_sy_hy_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSyHyEmProvider(BaseProvider):
    """行业商誉数据提供者"""
    
    # 必填属性
    collection_name = "stock_sy_hy_em"
    display_name = "行业商誉"
    akshare_func = "stock_sy_hy_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-商誉-行业商誉"
    collection_route = "/stocks/collections/stock_sy_hy_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "公司家数", "type": "int64", "description": "-"},
        {"name": "商誉规模", "type": "float64", "description": "-"},
        {"name": "净资产", "type": "float64", "description": "-"},
        {"name": "商誉规模占净资产规模比例", "type": "float64", "description": "-"},
        {"name": "净利润规模", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
