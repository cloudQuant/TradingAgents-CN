"""
董监高及相关人员持股变动明细数据提供者

东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细
接口: stock_hold_management_detail_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHoldManagementDetailEmProvider(SimpleProvider):
    """董监高及相关人员持股变动明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_hold_management_detail_em"
    display_name = "董监高及相关人员持股变动明细"
    akshare_func = "stock_hold_management_detail_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-高管持股-董监高及相关人员持股变动明细"
    collection_route = "/stocks/collections/stock_hold_management_detail_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "变动人", "type": "object", "description": "-"},
        {"name": "变动股数", "type": "int64", "description": "-"},
        {"name": "成交均价", "type": "int64", "description": "-"},
        {"name": "变动金额", "type": "float64", "description": "-"},
        {"name": "变动原因", "type": "object", "description": "-"},
        {"name": "变动比例", "type": "float64", "description": "-"},
        {"name": "变动后持股数", "type": "float64", "description": "-"},
        {"name": "持股种类", "type": "object", "description": "-"},
        {"name": "董监高人员姓名", "type": "object", "description": "-"},
        {"name": "职务", "type": "object", "description": "-"},
        {"name": "变动人与董监高的关系", "type": "object", "description": "-"},
        {"name": "开始时持有", "type": "float64", "description": "-"},
        {"name": "结束后持有", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
