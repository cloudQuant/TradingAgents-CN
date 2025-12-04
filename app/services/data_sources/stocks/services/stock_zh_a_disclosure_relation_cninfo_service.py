"""
信息披露调研-巨潮资讯服务

巨潮资讯-首页-公告查询-信息披露调研-沪深京
接口: stock_zh_a_disclosure_relation_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_disclosure_relation_cninfo_provider import StockZhADisclosureRelationCninfoProvider


class StockZhADisclosureRelationCninfoService(BaseService):
    """信息披露调研-巨潮资讯服务"""
    
    collection_name = "stock_zh_a_disclosure_relation_cninfo"
    provider_class = StockZhADisclosureRelationCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
