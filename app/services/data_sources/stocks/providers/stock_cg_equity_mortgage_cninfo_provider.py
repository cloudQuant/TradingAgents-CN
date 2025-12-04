"""
股权质押数据提供者

巨潮资讯-数据中心-专题统计-公司治理-股权质押
接口: stock_cg_equity_mortgage_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockCgEquityMortgageCninfoProvider(BaseProvider):
    """股权质押数据提供者"""
    
    # 必填属性
    collection_name = "stock_cg_equity_mortgage_cninfo"
    display_name = "股权质押"
    akshare_func = "stock_cg_equity_mortgage_cninfo"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-专题统计-公司治理-股权质押"
    collection_route = "/stocks/collections/stock_cg_equity_mortgage_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "公告日期", "type": "object", "description": "-"},
        {"name": "出质人", "type": "object", "description": "-"},
        {"name": "质权人", "type": "object", "description": "-"},
        {"name": "质押数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "质押解除数量", "type": "float64", "description": "注意单位: 万股"},
        {"name": "质押事项", "type": "object", "description": "注意单位: 万元"},
        {"name": "累计质押占总股本比例", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
