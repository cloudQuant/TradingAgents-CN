"""
科创板公告数据提供者

东方财富-科创板报告数据
接口: stock_zh_kcb_report_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhKcbReportEmProvider(BaseProvider):
    """科创板公告数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_kcb_report_em"
    display_name = "科创板公告"
    akshare_func = "stock_zh_kcb_report_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-科创板报告数据"
    collection_route = "/stocks/collections/stock_zh_kcb_report_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "from_page": "from_page",
        "to_page": "to_page"
    }
    
    # 必填参数
    required_params = ['from_page', 'to_page']

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "公告标题", "type": "object", "description": "-"},
        {"name": "公告类型", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "公告代码", "type": "object", "description": "本代码可以用来获取公告详情: http://data.eastmoney.com/notices/detail/688595/{替换到此处}.html"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
