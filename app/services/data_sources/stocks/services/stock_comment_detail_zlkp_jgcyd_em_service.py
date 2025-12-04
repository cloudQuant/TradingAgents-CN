"""
机构参与度服务

东方财富网-数据中心-特色数据-千股千评-主力控盘-机构参与度
接口: stock_comment_detail_zlkp_jgcyd_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_comment_detail_zlkp_jgcyd_em_provider import StockCommentDetailZlkpJgcydEmProvider


class StockCommentDetailZlkpJgcydEmService(BaseService):
    """机构参与度服务"""
    
    collection_name = "stock_comment_detail_zlkp_jgcyd_em"
    provider_class = StockCommentDetailZlkpJgcydEmProvider
    
    # 时间字段名
    time_field = "更新时间"
