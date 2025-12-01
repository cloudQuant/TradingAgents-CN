"""
货币型基金历史行情-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundMoneyFundInfoEmProvider(BaseProvider):
    
    """货币型基金历史行情-东财数据提供者"""

    collection_description = "东方财富网-天天基金网-货币型基金历史净值数据"
    collection_route = "/funds/collections/fund_money_fund_info_em"
    collection_order = 18

    collection_name = "fund_money_fund_info_em"
    display_name = "货币型基金历史行情-东方财富"
    akshare_func = "fund_money_fund_info_em"
    unique_keys = ["基金代码", "净值日期"]
    
    # 参数映射：多个前端参数映射到symbol（akshare函数需要symbol参数）
    param_mapping = {
        "fund_code": "symbol",
        "fund": "symbol",
        "code": "symbol",
        "symbol": "symbol",
    }
    required_params = ["symbol"]
    
    # 自动添加基金代码字段
    add_param_columns = {
        "symbol": "基金代码",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "净值日期", "type": "string", "description": "净值日期"},
        {"name": "每万份收益", "type": "float", "description": "每万份收益"},
        {"name": "7日年化收益率", "type": "float", "description": "7日年化收益率"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_money_fund_info_em"},
    ]
