"""
历史行情数据-东财服务

东方财富-沪深京 A 股日频率数据; 历史数据按日频率更新, 当日收盘价请在收盘后获取
接口: stock_zh_a_hist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_hist_provider import StockZhAHistProvider


class StockZhAHistService(BaseService):
    """历史行情数据-东财服务"""
    
    collection_name = "stock_zh_a_hist"
    provider_class = StockZhAHistProvider
    
    # 时间字段名
    time_field = "更新时间"
