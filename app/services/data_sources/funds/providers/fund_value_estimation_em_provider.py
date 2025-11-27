"""
基金净值估算-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundValueEstimationEmProvider(SimpleProvider):
    """基金净值估算-东财数据提供者"""
    
    collection_name = "fund_value_estimation_em"
    display_name = "基金净值估算-东财"
    akshare_func = "fund_value_estimation_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "交易日-估算数据-估算值", "type": "string", "description": ""},
        {"name": "交易日-估算数据-估算增长率", "type": "string", "description": ""},
        {"name": "交易日-公布数据-单位净值", "type": "string", "description": ""},
        {"name": "交易日-公布数据-日增长率", "type": "string", "description": ""},
        {"name": "估算偏差", "type": "string", "description": ""},
        {"name": "交易日-单位净值", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_value_estimation_em"},
    ]
