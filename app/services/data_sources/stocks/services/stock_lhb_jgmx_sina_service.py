"""
龙虎榜-机构席位成交明细服务

新浪财经-龙虎榜-机构席位成交明细
接口: stock_lhb_jgmx_sina
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_lhb_jgmx_sina_provider import StockLhbJgmxSinaProvider


class StockLhbJgmxSinaService(SimpleService):
    """龙虎榜-机构席位成交明细服务"""
    
    collection_name = "stock_lhb_jgmx_sina"
    provider_class = StockLhbJgmxSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
