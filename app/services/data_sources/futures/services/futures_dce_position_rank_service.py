"""大连商品交易所-持仓排名数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesDcePositionRankService(SimpleService):
    """大连商品交易所-持仓排名数据服务"""
    collection_name = "futures_dce_position_rank"
