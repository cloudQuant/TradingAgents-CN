"""广州期货交易所-持仓排名数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesGfexPositionRankService(SimpleService):
    """广州期货交易所-持仓排名数据服务"""
    collection_name = "futures_gfex_position_rank"
