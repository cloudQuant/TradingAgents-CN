"""
基金拆分-东财数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundCfEmProvider(BaseProvider):
    """基金拆分-东财数据提供者"""
    
    collection_name = "fund_cf_em"
    display_name = "基金拆分-东财"
    akshare_func = "fund_cf_em"
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
        {"name": "拆分折算日", "type": "string", "description": "拆分折算日"},
        {"name": "拆分类型", "type": "string", "description": "拆分类型"},
        {"name": "拆分折算比例", "type": "float", "description": "拆分折算比例"},
        {"name": "年份", "type": "string", "description": "年份"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_cf_em"},
    ]
