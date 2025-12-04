"""
融资融券汇总服务

上海证券交易所-融资融券数据-融资融券汇总数据
接口: stock_margin_sse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_sse_provider import StockMarginSseProvider


class StockMarginSseService(BaseService):
    """融资融券汇总服务"""
    
    collection_name = "stock_margin_sse"
    provider_class = StockMarginSseProvider
    
    # 时间字段名
    time_field = "更新时间"
