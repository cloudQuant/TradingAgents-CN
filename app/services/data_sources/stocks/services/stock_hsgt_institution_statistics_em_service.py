"""
机构排行服务

东方财富网-数据中心-沪深港通-沪深港通持股-机构排行
接口: stock_hsgt_institution_statistics_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_institution_statistics_em_provider import StockHsgtInstitutionStatisticsEmProvider


class StockHsgtInstitutionStatisticsEmService(BaseService):
    """机构排行服务"""
    
    collection_name = "stock_hsgt_institution_statistics_em"
    provider_class = StockHsgtInstitutionStatisticsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
