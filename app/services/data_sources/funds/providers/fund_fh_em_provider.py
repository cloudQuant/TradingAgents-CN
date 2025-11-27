"""
基金分红-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundFhEmProvider(BaseProvider):
    """基金分红-东财数据提供者"""
    
    collection_name = "fund_fh_em"
    display_name = "基金分红-东财"
    akshare_func = "fund_fh_em"
    unique_keys = ["基金代码", "更新时间"]
    
    # 参数映射：year/date 都映射到 date
    param_mapping = {
        "year": "date",
        "date": "date",
    }
    required_params = ["date"]
    
    # 自动添加年份字段
    add_param_columns = {
        "date": "年份",
    }
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "分红发放日", "type": "string", "description": "分红发放日"},
        {"name": "分红方案", "type": "string", "description": "分红方案"},
        {"name": "年份", "type": "string", "description": "年份"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_fh_em"},
    ]
