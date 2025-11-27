"""
基金行业配置-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundPortfolioIndustryAllocationEmProvider(SimpleProvider):
    """基金行业配置-东财数据提供者"""
    
    collection_name = "fund_portfolio_industry_allocation_em"
    display_name = "基金行业配置-东财"
    akshare_func = "fund_portfolio_industry_allocation_em"
    unique_keys = ["截止时间"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "行业类别", "type": "string", "description": ""},
        {"name": "占净值比例", "type": "float", "description": "注意单位: %"},
        {"name": "市值", "type": "float", "description": "注意单位: 万元"},
        {"name": "截止时间", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_portfolio_industry_allocation_em"},
    ]
