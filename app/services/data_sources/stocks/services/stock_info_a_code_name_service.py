"""
股票列表-A股服务

沪深京 A 股股票代码和股票简称数据
接口: stock_info_a_code_name
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_info_a_code_name_provider import StockInfoACodeNameProvider


class StockInfoACodeNameService(SimpleService):
    """股票列表-A股服务"""
    
    collection_name = "stock_info_a_code_name"
    provider_class = StockInfoACodeNameProvider
    
    # 时间字段名
    time_field = "更新时间"
