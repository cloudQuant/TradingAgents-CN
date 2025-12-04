"""
分红情况-同花顺数据提供者

同花顺-分红情况
接口: stock_fhps_detail_ths
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFhpsDetailThsProvider(BaseProvider):
    """分红情况-同花顺数据提供者"""
    
    # 必填属性
    collection_name = "stock_fhps_detail_ths"
    display_name = "分红情况-同花顺"
    akshare_func = "stock_fhps_detail_ths"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "同花顺-分红情况"
    collection_route = "/stocks/collections/stock_fhps_detail_ths"
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
        {"name": "报告期", "type": "object", "description": "-"},
        {"name": "董事会日期", "type": "object", "description": "-"},
        {"name": "股东大会预案公告日期", "type": "object", "description": "-"},
        {"name": "实施公告日", "type": "object", "description": "-"},
        {"name": "分红方案说明", "type": "object", "description": "-"},
        {"name": "A股股权登记日", "type": "object", "description": "注意: 根据 A 股和 B 股变化"},
        {"name": "A股除权除息日", "type": "object", "description": "注意: 根据 A 股和 B 股变化"},
        {"name": "分红总额", "type": "object", "description": "-"},
        {"name": "方案进度", "type": "object", "description": "-"},
        {"name": "股利支付率", "type": "object", "description": "-"},
        {"name": "税前分红率", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
