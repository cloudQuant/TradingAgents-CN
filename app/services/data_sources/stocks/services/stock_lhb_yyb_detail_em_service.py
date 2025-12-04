"""
营业部详情数据-东财服务

东方财富网-数据中心-龙虎榜单-营业部历史交易明细-营业部交易明细
接口: stock_lhb_yyb_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_yyb_detail_em_provider import StockLhbYybDetailEmProvider


class StockLhbYybDetailEmService(BaseService):
    """营业部详情数据-东财服务"""
    
    collection_name = "stock_lhb_yyb_detail_em"
    provider_class = StockLhbYybDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
