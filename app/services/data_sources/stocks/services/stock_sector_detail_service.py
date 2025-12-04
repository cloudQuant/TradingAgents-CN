"""
板块详情服务

新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数
接口: stock_sector_detail
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sector_detail_provider import StockSectorDetailProvider


class StockSectorDetailService(BaseService):
    """板块详情服务"""
    
    collection_name = "stock_sector_detail"
    provider_class = StockSectorDetailProvider
    
    # 时间字段名
    time_field = "更新时间"
