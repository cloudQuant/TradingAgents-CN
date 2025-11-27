"""
分级基金历史数据-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundGradedFundInfoEmProvider(SimpleProvider):
    """分级基金历史数据-东财数据提供者"""
    
    collection_name = "fund_graded_fund_info_em"
    display_name = "分级基金历史数据-东财"
    akshare_func = "fund_graded_fund_info_em"
    unique_keys = ["净值日期"]

    field_info = [
        {"name": "净值日期", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "累计净值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %; 日增长率为空原因如下: 1. 非交易日净值不参与日增长率计算(灰色数据行). 2. 上一交易日净值未披露, 日增长率无法计算."},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_graded_fund_info_em"},
    ]
