"""
龙虎榜-每日详情服务

新浪财经-龙虎榜-每日详情
接口: stock_lhb_detail_daily_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_detail_daily_sina_provider import StockLhbDetailDailySinaProvider


class StockLhbDetailDailySinaService(BaseService):
    """龙虎榜-每日详情服务"""
    
    collection_name = "stock_lhb_detail_daily_sina"
    provider_class = StockLhbDetailDailySinaProvider
    
    # 时间字段名
    time_field = "更新时间"
