"""
实时行情数据-新浪服务

新浪财经-沪深京 A 股数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
接口: stock_zh_a_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_spot_provider import StockZhASpotProvider


class StockZhASpotService(SimpleService):
    """实时行情数据-新浪服务"""
    
    collection_name = "stock_zh_a_spot"
    provider_class = StockZhASpotProvider
    
    # 时间字段名
    time_field = "更新时间"
