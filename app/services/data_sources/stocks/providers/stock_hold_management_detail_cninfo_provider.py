"""
高管持股变动明细数据提供者

巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细
接口: stock_hold_management_detail_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHoldManagementDetailCninfoProvider(BaseProvider):
    """高管持股变动明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_hold_management_detail_cninfo"
    display_name = "高管持股变动明细"
    akshare_func = "stock_hold_management_detail_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-股东股本-高管持股变动明细"
    collection_route = "/stocks/collections/stock_hold_management_detail_cninfo"
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
        {"name": "证劵代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "截止日期", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "高管姓名", "type": "object", "description": "-"},
        {"name": "董监高姓名", "type": "object", "description": "-"},
        {"name": "董监高职务", "type": "object", "description": "-"},
        {"name": "变动人与董监高关系", "type": "object", "description": "-"},
        {"name": "期初持股数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "期末持股数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "变动数量", "type": "float64", "description": "-"},
        {"name": "变动比例", "type": "int64", "description": "注意单位: %"},
        {"name": "成交均价", "type": "float64", "description": "注意单位: 元"},
        {"name": "期末市值", "type": "float64", "description": "注意单位: 万元"},
        {"name": "持股变动原因", "type": "object", "description": "-"},
        {"name": "数据来源", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
