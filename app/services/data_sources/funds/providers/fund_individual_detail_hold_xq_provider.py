"""
基金持仓明细-雪球数据提供者（重构版：继承BaseProvider，需要symbol和date参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundIndividualDetailHoldXqProvider(BaseProvider):
    """基金持仓明细-雪球数据提供者（需要基金代码和季度日期参数）"""

    collection_description = "雪球基金-基金详情-持仓资产比例（需要基金代码和季度日期，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_individual_detail_hold_xq"
    collection_order = 39

    collection_name = "fund_individual_detail_hold_xq"
    display_name = "基金持仓资产比例-雪球"
    akshare_func = "fund_individual_detail_hold_xq"
    
    # 唯一键：基金代码 + 季度日期 + 资产类别
    unique_keys = ["基金代码", "季度日期", "资产类别"]
    
    # 参数映射：symbol/fund_code/code 都映射到 symbol，date/quarter_date 映射到 date
    param_mapping = {
        "symbol": "symbol",
        "fund_code": "symbol",
        "code": "symbol",
        "date": "date",
        "quarter_date": "date",
    }
    required_params = ["symbol", "date"]
    
    # 自动添加参数列：将symbol参数值写入"基金代码"列，date参数值写入"季度日期"列
    add_param_columns = {
        "symbol": "基金代码",
        "date": "季度日期",
    }

    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码（如 000001）"},
        {"name": "季度日期", "type": "string", "description": "季度日期（如 2024-03-31）"},
        {"name": "资产类别", "type": "string", "description": "资产类别"},
        {"name": "仓位占比", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_detail_hold_xq"},
    ]
