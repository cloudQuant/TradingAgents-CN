"""
基金分析数据-雪球数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundIndividualAnalysisXqProvider(SimpleProvider):
    """基金分析数据-雪球数据提供者"""
    
    collection_name = "fund_individual_analysis_xq"
    display_name = "基金分析数据-雪球"
    akshare_func = "fund_individual_analysis_xq"
    unique_keys = ["更新时间"]

    field_info = [
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
