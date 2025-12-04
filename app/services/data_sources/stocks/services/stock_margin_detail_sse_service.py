"""
融资融券明细服务

上海证券交易所-融资融券数据-融资融券明细数据
接口: stock_margin_detail_sse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_margin_detail_sse_provider import StockMarginDetailSseProvider


class StockMarginDetailSseService(BaseService):
    """融资融券明细服务"""
    
    collection_name = "stock_margin_detail_sse"
    provider_class = StockMarginDetailSseProvider
    
    # 时间字段名
    time_field = "更新时间"
