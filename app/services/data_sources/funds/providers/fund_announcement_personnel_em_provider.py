"""
基金人事公告-东财数据提供者（重构版：继承BaseProvider，需要symbol参数）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundAnnouncementPersonnelEmProvider(BaseProvider):
    """基金人事公告-东财数据提供者（需要基金代码参数）"""

    collection_description = "东方财富网站-天天基金网-基金档案-基金公告-人事调整（需要基金代码，支持单个/批量更新）"
    collection_route = "/funds/collections/fund_announcement_personnel_em"
    collection_order = 71

    collection_name = "fund_announcement_personnel_em"
    display_name = "基金公告人事调整-东财"
    akshare_func = "fund_announcement_personnel_em"
    
    # 唯一键：基金代码 + 报告ID（报告ID应该是唯一的）
    unique_keys = ["基金代码", "报告ID"]
    
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
    
    # 自定义时间戳字段名
    timestamp_field = "更新时间"

    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "公告标题", "type": "string", "description": "公告标题"},
        {"name": "基金名称", "type": "string", "description": "基金名称"},
        {"name": "公告日期", "type": "string", "description": "公告的发布日期"},
        {"name": "报告ID", "type": "string", "description": "获取报告详情的依据; 拼接后可以获取公告地址"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_announcement_personnel_em"},
    ]
