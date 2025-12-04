"""
新股发行数据提供者

新浪财经-发行与分配-新股发行
接口: stock_ipo_info
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIpoInfoProvider(BaseProvider):
    """新股发行数据提供者"""
    
    # 必填属性
    collection_name = "stock_ipo_info"
    display_name = "新股发行"
    akshare_func = "stock_ipo_info"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-发行与分配-新股发行"
    collection_route = "/stocks/collections/stock_ipo_info"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "stock": "stock"
    }
    
    # 必填参数
    required_params = ['stock']

    # 字段信息
    field_info = [
        {"name": "item", "type": "object", "description": "所列项目"},
        {"name": "value", "type": "object", "description": "项目值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
