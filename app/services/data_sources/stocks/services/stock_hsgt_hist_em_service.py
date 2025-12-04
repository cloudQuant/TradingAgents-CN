"""
沪深港通历史数据服务

东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
接口: stock_hsgt_hist_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_hist_em_provider import StockHsgtHistEmProvider


class StockHsgtHistEmService(BaseService):
    """沪深港通历史数据服务"""
    
    collection_name = "stock_hsgt_hist_em"
    provider_class = StockHsgtHistEmProvider
    
    # 时间字段名
    time_field = "更新时间"
