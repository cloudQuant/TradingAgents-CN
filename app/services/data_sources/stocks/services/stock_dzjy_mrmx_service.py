"""
每日明细服务

东方财富网-数据中心-大宗交易-每日明细
接口: stock_dzjy_mrmx
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dzjy_mrmx_provider import StockDzjyMrmxProvider


class StockDzjyMrmxService(BaseService):
    """每日明细服务"""
    
    collection_name = "stock_dzjy_mrmx"
    provider_class = StockDzjyMrmxProvider
    
    # 时间字段名
    time_field = "更新时间"
