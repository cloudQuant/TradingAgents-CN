"""
盘前数据服务

东方财富-股票行情-盘前数据
接口: stock_zh_a_hist_pre_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_hist_pre_min_em_provider import StockZhAHistPreMinEmProvider


class StockZhAHistPreMinEmService(BaseService):
    """盘前数据服务"""
    
    collection_name = "stock_zh_a_hist_pre_min_em"
    provider_class = StockZhAHistPreMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
