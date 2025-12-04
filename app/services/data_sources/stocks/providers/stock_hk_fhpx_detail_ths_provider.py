"""
分红配送详情-港股-同花顺数据提供者

同花顺-港股-分红派息
接口: stock_hk_fhpx_detail_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHkFhpxDetailThsProvider(BaseProvider):
    """分红配送详情-港股-同花顺数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_fhpx_detail_ths"
    display_name = "分红配送详情-港股-同花顺"
    akshare_func = "stock_hk_fhpx_detail_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-港股-分红派息"
    collection_route = "/stocks/collections/stock_hk_fhpx_detail_ths"
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
        {"name": "方案", "type": "object", "description": "-"},
        {"name": "除净日", "type": "object", "description": "-"},
        {"name": "派息日", "type": "object", "description": "-"},
        {"name": "过户日期起止日-起始", "type": "object", "description": "-"},
        {"name": "过户日期起止日-截止", "type": "object", "description": "-"},
        {"name": "类型", "type": "object", "description": "-"},
        {"name": "进度", "type": "object", "description": "-"},
        {"name": "以股代息", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
