"""
新股发行数据提供者

巨潮资讯-数据中心-新股数据-新股发行
接口: stock_new_ipo_cninfo
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockNewIpoCninfoProvider(SimpleProvider):
    """新股发行数据提供者"""
    
    # 必填属性
    collection_name = "stock_new_ipo_cninfo"
    display_name = "新股发行"
    akshare_func = "stock_new_ipo_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-新股数据-新股发行"
    collection_route = "/stocks/collections/stock_new_ipo_cninfo"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "证劵代码", "type": "object", "description": "-"},
        {"name": "证券简称", "type": "object", "description": "-"},
        {"name": "上市日期", "type": "object", "description": "-"},
        {"name": "申购日期", "type": "object", "description": "-"},
        {"name": "发行价", "type": "float64", "description": "注意单位: 元"},
        {"name": "总发行数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "发行市盈率", "type": "float64", "description": "-"},
        {"name": "上网发行中签率", "type": "float64", "description": "注意单位: %"},
        {"name": "摇号结果公告日", "type": "object", "description": "-"},
        {"name": "中签公告日", "type": "object", "description": "-"},
        {"name": "中签缴款日", "type": "object", "description": "-"},
        {"name": "网上申购上限", "type": "float64", "description": "-"},
        {"name": "上网发行数量", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
