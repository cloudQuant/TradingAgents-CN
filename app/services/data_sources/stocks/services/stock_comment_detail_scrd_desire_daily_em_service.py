"""
日度市场参与意愿服务

东方财富网-数据中心-特色数据-千股千评-市场热度-日度市场参与意愿
接口: stock_comment_detail_scrd_desire_daily_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_comment_detail_scrd_desire_daily_em_provider import StockCommentDetailScrdDesireDailyEmProvider


class StockCommentDetailScrdDesireDailyEmService(BaseService):
    """日度市场参与意愿服务"""
    
    collection_name = "stock_comment_detail_scrd_desire_daily_em"
    provider_class = StockCommentDetailScrdDesireDailyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
