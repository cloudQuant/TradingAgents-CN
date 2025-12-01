"""
基金概况-东财数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundOverviewEmProvider(BaseProvider):
    """基金概况-东财数据提供者（需要基金代码参数）"""

    collection_description = "东方财富网-数据中心-基金基本概况（需要基金代码，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_overview_em"
    collection_order = 40

    collection_name = "fund_overview_em"
    display_name = "基金基本概况-东财"
    akshare_func = "fund_overview_em"
    
    # 唯一键：基金代码
    unique_keys = ["基金代码"]
    
    # 参数映射：symbol/fund_code/code 都映射到 symbol
    param_mapping = {
        "symbol": "symbol",
        "fund_code": "symbol",
        "code": "symbol",
    }
    required_params = ["symbol"]
    
    # 自动添加参数列：将symbol参数值写入"基金代码"列
    add_param_columns = {
        "symbol": "基金代码",
    }

    field_info = [
        {"name": "基金全称", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "发行日期", "type": "string", "description": ""},
        {"name": "成立日期/规模", "type": "string", "description": ""},
        {"name": "资产规模", "type": "string", "description": ""},
        {"name": "份额规模", "type": "string", "description": ""},
        {"name": "基金管理人", "type": "string", "description": ""},
        {"name": "基金托管人", "type": "string", "description": ""},
        {"name": "基金经理人", "type": "string", "description": ""},
        {"name": "成立来分红", "type": "string", "description": ""},
        {"name": "管理费率", "type": "string", "description": ""},
        {"name": "托管费率", "type": "string", "description": ""},
        {"name": "销售服务费率", "type": "string", "description": ""},
        {"name": "最高认购费率", "type": "string", "description": ""},
        {"name": "业绩比较基准", "type": "string", "description": ""},
        {"name": "跟踪标的", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_overview_em"},
    ]
