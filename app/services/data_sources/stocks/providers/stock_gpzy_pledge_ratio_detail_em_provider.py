"""
重要股东股权质押明细数据提供者

东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细
接口: stock_gpzy_pledge_ratio_detail_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockGpzyPledgeRatioDetailEmProvider(SimpleProvider):
    """重要股东股权质押明细数据提供者"""
    
    # 必填属性
    collection_name = "stock_gpzy_pledge_ratio_detail_em"
    display_name = "重要股东股权质押明细"
    akshare_func = "stock_gpzy_pledge_ratio_detail_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-特色数据-股权质押-重要股东股权质押明细"
    collection_route = "/stocks/collections/stock_gpzy_pledge_ratio_detail_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "质押股份数量", "type": "float64", "description": "注意单位: 股"},
        {"name": "占所持股份比例", "type": "float64", "description": "注意单位: %"},
        {"name": "占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "质押机构", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 元"},
        {"name": "质押日收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "预估平仓线", "type": "float64", "description": "注意单位: 元"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "质押开始日期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
