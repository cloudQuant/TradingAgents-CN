"""成交持仓-新浪数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHoldPosSinaService(SimpleService):
    """成交持仓-新浪数据服务"""
    collection_name = "futures_hold_pos_sina"
