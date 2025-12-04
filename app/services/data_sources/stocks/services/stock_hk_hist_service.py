"""
历史行情数据-东财服务

港股-历史行情数据, 可以选择返回复权后数据, 更新频率为日频
接口: stock_hk_hist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_hist_provider import StockHkHistProvider


class StockHkHistService(BaseService):
    """历史行情数据-东财服务"""
    
    collection_name = "stock_hk_hist"
    provider_class = StockHkHistProvider
    
    # 时间字段名
    time_field = "更新时间"
