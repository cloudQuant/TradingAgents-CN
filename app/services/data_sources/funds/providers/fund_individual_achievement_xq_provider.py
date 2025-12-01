"""
基金业绩表现-雪球数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundIndividualAchievementXqProvider(BaseProvider):
    """基金业绩表现-雪球数据提供者（需要基金代码参数）"""

    collection_description = "雪球基金-基金详情-基金业绩-详情（需要基金代码，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_individual_achievement_xq"
    collection_order = 35

    collection_name = "fund_individual_achievement_xq"
    display_name = "基金业绩-雪球"
    akshare_func = "fund_individual_achievement_xq"
    
    # 唯一键：代码 + 业绩类型 + 周期（因为同一个基金有多个业绩记录）
    unique_keys = ["代码", "业绩类型", "周期"]
    
    # 参数映射：symbol/fund_code/code 都映射到 symbol
    param_mapping = {
        "symbol": "symbol",
        "fund_code": "symbol",
        "code": "symbol",
    }
    required_params = ["symbol"]
    
    # 自动添加参数列：将symbol参数值写入"代码"列
    add_param_columns = {
        "symbol": "代码",
    }

    field_info = [
        {"name": "代码", "type": "string", "description": "基金代码（如 000001）"},
        {"name": "业绩类型", "type": "string", "description": ""},
        {"name": "周期", "type": "string", "description": ""},
        {"name": "本产品区间收益", "type": "float", "description": "注意单位: %"},
        {"name": "本产品最大回撒", "type": "float", "description": "注意单位: %"},
        {"name": "周期收益同类排名", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_achievement_xq"},
    ]
