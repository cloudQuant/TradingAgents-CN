"""
实时行情数据-新浪服务

B 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
接口: stock_zh_b_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_b_spot_provider import StockZhBSpotProvider


class StockZhBSpotService(SimpleService):
    """实时行情数据-新浪服务"""
    
    collection_name = "stock_zh_b_spot"
    provider_class = StockZhBSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
