"""
巴菲特指标服务

乐估乐股-底部研究-巴菲特指标
接口: stock_buffett_index_lg
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_buffett_index_lg_provider import StockBuffettIndexLgProvider


class StockBuffettIndexLgService(SimpleService):
    """巴菲特指标服务"""
    
    collection_name = "stock_buffett_index_lg"
    provider_class = StockBuffettIndexLgProvider
    
    # 时间字段名
    time_field = "更新时间"
