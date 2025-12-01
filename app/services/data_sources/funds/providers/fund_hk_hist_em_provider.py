"""
香港基金历史数据-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundHkHistEmProvider(BaseProvider):
    
    """香港基金历史数据-东财数据提供者"""

    collection_description = "东方财富网-天天基金网-香港基金-历史净值明细和分红送配详情"
    collection_route = "/funds/collections/fund_hk_hist_em"
    collection_order = 24

    collection_name = "fund_hk_hist_em"
    display_name = "香港基金-历史数据"
    akshare_func = "fund_hk_fund_hist_em"  # 修正：正确的接口名称
    unique_keys = ["code", "symbol", "净值日期"]  # 添加 code 和 symbol 作为唯一键的一部分
    
    # 参数映射：多个前端参数映射到 code 和 symbol
    param_mapping = {
        "fund_code": "code",
        "fund": "code",
        "code": "code",
    }
    required_params = ["code", "symbol"]  # 必填参数：code 和 symbol
    
    # 自动添加 code 和 symbol 字段到数据中
    add_param_columns = {
        "code": "code",  # 将 code 参数值写入 "code" 列
        "symbol": "symbol",  # 将 symbol 参数值写入 "symbol" 列
    }

    field_info = [
        {"name": "code", "type": "string", "description": "香港基金代码"},
        {"name": "symbol", "type": "string", "description": "数据类型：历史净值明细 或 分红送配详情"},
        {"name": "净值日期", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "日增长值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "单位", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_hk_fund_hist_em"},
    ]
