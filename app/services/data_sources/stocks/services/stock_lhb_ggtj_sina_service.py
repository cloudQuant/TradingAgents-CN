"""
龙虎榜-个股上榜统计服务

新浪财经-龙虎榜-个股上榜统计
接口: stock_lhb_ggtj_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_ggtj_sina_provider import StockLhbGgtjSinaProvider


class StockLhbGgtjSinaService(BaseService):
    """龙虎榜-个股上榜统计服务"""
    
    collection_name = "stock_lhb_ggtj_sina"
    provider_class = StockLhbGgtjSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
