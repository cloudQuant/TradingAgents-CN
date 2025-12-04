"""
A 股等权重与中位数市盈率服务

乐咕乐股-A 股等权重市盈率与中位数市盈率
接口: stock_a_ttm_lyr
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_a_ttm_lyr_provider import StockATtmLyrProvider


class StockATtmLyrService(SimpleService):
    """A 股等权重与中位数市盈率服务"""
    
    collection_name = "stock_a_ttm_lyr"
    provider_class = StockATtmLyrProvider
    
    # 时间字段名
    time_field = "更新时间"
