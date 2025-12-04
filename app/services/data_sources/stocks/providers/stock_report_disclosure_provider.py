"""
预约披露时间-巨潮资讯数据提供者

巨潮资讯-数据-预约披露的数据
接口: stock_report_disclosure
"""
from app.services.data_sources.base_provider import BaseProvider


class StockReportDisclosureProvider(BaseProvider):
    """预约披露时间-巨潮资讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_report_disclosure"
    display_name = "预约披露时间-巨潮资讯"
    akshare_func = "stock_report_disclosure"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据-预约披露的数据"
    collection_route = "/stocks/collections/stock_report_disclosure"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "market": "market",
        "period": "period"
    }
    
    # 必填参数
    required_params = ['market', 'period']

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "首次预约", "type": "object", "description": "-"},
        {"name": "初次变更", "type": "object", "description": "-"},
        {"name": "二次变更", "type": "object", "description": "-"},
        {"name": "三次变更", "type": "object", "description": "-"},
        {"name": "实际披露", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
