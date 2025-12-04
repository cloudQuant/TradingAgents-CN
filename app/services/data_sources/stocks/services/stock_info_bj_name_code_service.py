"""
股票列表-北证服务

北京证券交易所股票代码和简称数据
接口: stock_info_bj_name_code
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_info_bj_name_code_provider import StockInfoBjNameCodeProvider


class StockInfoBjNameCodeService(SimpleService):
    """股票列表-北证服务"""
    
    collection_name = "stock_info_bj_name_code"
    provider_class = StockInfoBjNameCodeProvider
    
    # 时间字段名
    time_field = "更新时间"
