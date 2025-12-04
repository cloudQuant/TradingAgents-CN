"""
龙虎榜-营业上榜统计服务

新浪财经-龙虎榜-营业上榜统计
接口: stock_lhb_yytj_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_yytj_sina_provider import StockLhbYytjSinaProvider


class StockLhbYytjSinaService(BaseService):
    """龙虎榜-营业上榜统计服务"""
    
    collection_name = "stock_lhb_yytj_sina"
    provider_class = StockLhbYytjSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
