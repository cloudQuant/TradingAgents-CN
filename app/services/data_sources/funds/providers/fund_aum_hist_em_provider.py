"""
基金规模历史-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundAumHistEmProvider(SimpleProvider):
    """基金规模历史-东财数据提供者"""
    
    collection_name = "fund_aum_hist_em"
    display_name = "基金规模历史-东财"
    akshare_func = "fund_aum_hist_em"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金公司", "type": "string", "description": ""},
        {"name": "总规模", "type": "float", "description": ""},
        {"name": "股票型", "type": "float", "description": ""},
        {"name": "混合型", "type": "float", "description": ""},
        {"name": "债券型", "type": "float", "description": ""},
        {"name": "指数型", "type": "float", "description": ""},
        {"name": "QDII", "type": "float", "description": ""},
        {"name": "货币型", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_aum_hist_em"},
    ]
