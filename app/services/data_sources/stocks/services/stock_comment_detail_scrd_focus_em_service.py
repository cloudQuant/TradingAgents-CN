"""
用户关注指数服务

东方财富网-数据中心-特色数据-千股千评-市场热度-用户关注指数
接口: stock_comment_detail_scrd_focus_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_comment_detail_scrd_focus_em_provider import StockCommentDetailScrdFocusEmProvider


class StockCommentDetailScrdFocusEmService(BaseService):
    """用户关注指数服务"""
    
    collection_name = "stock_comment_detail_scrd_focus_em"
    provider_class = StockCommentDetailScrdFocusEmProvider
    
    # 时间字段名
    time_field = "更新时间"
