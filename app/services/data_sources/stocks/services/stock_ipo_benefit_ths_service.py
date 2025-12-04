"""
IPO 受益股服务

同花顺-数据中心-新股数据-IPO受益股
接口: stock_ipo_benefit_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_ipo_benefit_ths_provider import StockIpoBenefitThsProvider


class StockIpoBenefitThsService(SimpleService):
    """IPO 受益股服务"""
    
    collection_name = "stock_ipo_benefit_ths"
    provider_class = StockIpoBenefitThsProvider
    
    # 时间字段名
    time_field = "更新时间"
