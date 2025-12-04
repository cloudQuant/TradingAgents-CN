"""
对外担保服务

巨潮资讯-数据中心-专题统计-公司治理-对外担保
接口: stock_cg_guarantee_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cg_guarantee_cninfo_provider import StockCgGuaranteeCninfoProvider


class StockCgGuaranteeCninfoService(BaseService):
    """对外担保服务"""
    
    collection_name = "stock_cg_guarantee_cninfo"
    provider_class = StockCgGuaranteeCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
