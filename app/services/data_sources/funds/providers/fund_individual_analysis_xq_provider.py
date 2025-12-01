"""
基金分析数据-雪球数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundIndividualAnalysisXqProvider(BaseProvider):
    """基金分析数据-雪球数据提供者（需要基金代码参数）"""

    collection_description = "雪球基金-基金详情-数据分析（需要基金代码，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_individual_analysis_xq"
    collection_order = 37

    collection_name = "fund_individual_analysis_xq"
    display_name = "基金数据分析-雪球"
    akshare_func = "fund_individual_analysis_xq"
    
    # 唯一键：基金代码 + 周期 + 更新时间
    unique_keys = ["基金代码", "周期", "更新时间"]
    
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
        {"name": "基金代码", "type": "string", "description": "基金代码（如 000001）"},
        {"name": "周期", "type": "string", "description": ""},
        {"name": "较同类风险收益比", "type": "string", "description": ""},
        {"name": "较同类抗风险波动", "type": "string", "description": ""},
        {"name": "年化波动率", "type": "string", "description": ""},
        {"name": "年化夏普比率", "type": "string", "description": ""},
        {"name": "最大回撤", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_analysis_xq"},
    ]
