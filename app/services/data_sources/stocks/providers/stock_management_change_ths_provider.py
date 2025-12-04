"""
高管持股变动统计数据提供者

同花顺-公司大事-高管持股变动
接口: stock_management_change_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockManagementChangeThsProvider(BaseProvider):
    """高管持股变动统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_management_change_ths"
    display_name = "高管持股变动统计"
    akshare_func = "stock_management_change_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-公司大事-高管持股变动"
    collection_route = "/stocks/collections/stock_management_change_ths"
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
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "变动人", "type": "object", "description": "-"},
        {"name": "与公司高管关系", "type": "object", "description": "-"},
        {"name": "变动数量", "type": "object", "description": "注意单位: 股"},
        {"name": "交易均价", "type": "object", "description": "注意单位: 元"},
        {"name": "剩余股数", "type": "object", "description": "注意单位: 股"},
        {"name": "变动途径", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
