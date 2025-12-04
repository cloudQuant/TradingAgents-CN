"""
龙虎榜-机构席位追踪服务

新浪财经-龙虎榜-机构席位追踪
接口: stock_lhb_jgzz_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_jgzz_sina_provider import StockLhbJgzzSinaProvider


class StockLhbJgzzSinaService(BaseService):
    """龙虎榜-机构席位追踪服务"""
    
    collection_name = "stock_lhb_jgzz_sina"
    provider_class = StockLhbJgzzSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
