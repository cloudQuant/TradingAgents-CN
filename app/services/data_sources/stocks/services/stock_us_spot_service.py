"""
实时行情数据-新浪服务

新浪财经-美股; 获取的数据有 15 分钟延迟; 建议使用 ak.stock_us_spot_em() 来获取数据
接口: stock_us_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_us_spot_provider import StockUsSpotProvider


class StockUsSpotService(SimpleService):
    """实时行情数据-新浪服务"""
    
    collection_name = "stock_us_spot"
    provider_class = StockUsSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
