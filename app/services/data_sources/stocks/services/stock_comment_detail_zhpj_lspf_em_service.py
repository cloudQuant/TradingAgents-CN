"""
历史评分服务

东方财富网-数据中心-特色数据-千股千评-综合评价-历史评分
接口: stock_comment_detail_zhpj_lspf_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_comment_detail_zhpj_lspf_em_provider import StockCommentDetailZhpjLspfEmProvider


class StockCommentDetailZhpjLspfEmService(BaseService):
    """历史评分服务"""
    
    collection_name = "stock_comment_detail_zhpj_lspf_em"
    provider_class = StockCommentDetailZhpjLspfEmProvider
    
    # 时间字段名
    time_field = "更新时间"
