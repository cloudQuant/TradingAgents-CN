"""
千股千评服务

东方财富网-数据中心-特色数据-千股千评
接口: stock_comment_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_comment_em_provider import StockCommentEmProvider


class StockCommentEmService(SimpleService):
    """千股千评服务"""
    
    collection_name = "stock_comment_em"
    provider_class = StockCommentEmProvider
    
    # 时间字段名
    time_field = "更新时间"
