"""
历史行情数据-新浪服务

新浪财经-沪深京 A 股的数据, 历史数据按日频率更新; 注意其中的 **sh689009** 为 CDR, 请 通过 **ak.stock_zh_a_cdr_daily** 接口获取
接口: stock_zh_a_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_daily_provider import StockZhADailyProvider


class StockZhADailyService(BaseService):
    """历史行情数据-新浪服务"""
    
    collection_name = "stock_zh_a_daily"
    provider_class = StockZhADailyProvider
    
    # 时间字段名
    time_field = "更新时间"
