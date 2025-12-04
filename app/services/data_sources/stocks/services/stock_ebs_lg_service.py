"""
股债利差服务

乐咕乐股-股债利差
接口: stock_ebs_lg
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_ebs_lg_provider import StockEbsLgProvider


class StockEbsLgService(SimpleService):
    """股债利差服务"""
    
    collection_name = "stock_ebs_lg"
    provider_class = StockEbsLgProvider
    
    # 时间字段名
    time_field = "更新时间"
