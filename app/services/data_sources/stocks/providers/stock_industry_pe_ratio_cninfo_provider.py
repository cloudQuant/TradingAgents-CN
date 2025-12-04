"""
行业市盈率数据提供者

巨潮资讯-数据中心-行业分析-行业市盈率
接口: stock_industry_pe_ratio_cninfo
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIndustryPeRatioCninfoProvider(BaseProvider):
    """行业市盈率数据提供者"""
    
    # 必填属性
    collection_name = "stock_industry_pe_ratio_cninfo"
    display_name = "行业市盈率"
    akshare_func = "stock_industry_pe_ratio_cninfo"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "巨潮资讯-数据中心-行业分析-行业市盈率"
    collection_route = "/stocks/collections/stock_industry_pe_ratio_cninfo"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "变动日期", "type": "object", "description": "-"},
        {"name": "行业分类", "type": "object", "description": "-"},
        {"name": "行业层级", "type": "int64", "description": "-"},
        {"name": "行业编码", "type": "object", "description": "-"},
        {"name": "公司数量", "type": "float64", "description": "-"},
        {"name": "纳入计算公司数量", "type": "float64", "description": "-"},
        {"name": "总市值-静态", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "净利润-静态", "type": "float64", "description": "注意单位: 亿元"},
        {"name": "静态市盈率-加权平均", "type": "float64", "description": "-"},
        {"name": "静态市盈率-中位数", "type": "float64", "description": "-"},
        {"name": "静态市盈率-算术平均", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
