"""
基金基本信息-东财数据提供者 (使用基类重构版本)

对比原版本 fund_name_em_provider.py（50行），新版本只需要约15行代码。
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundNameEmProviderV2(SimpleProvider):
    """基金基本信息-东财数据提供者"""
    
    collection_name = "fund_name_em"
    display_name = "基金基本信息-东财"
    akshare_func = "fund_name_em"
    unique_keys = ["基金代码"]
    
    field_info = [
        {"name": "基金代码", "type": "string", "description": "基金代码"},
        {"name": "基金简称", "type": "string", "description": "基金简称"},
        {"name": "基金类型", "type": "string", "description": "基金类型"},
        {"name": "拼音缩写", "type": "string", "description": "拼音缩写"},
        {"name": "scraped_at", "type": "datetime", "description": "抓取时间"},
    ]
