"""
股票列表-深证服务

深证证券交易所股票代码和股票简称数据
接口: stock_info_sz_name_code
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_sz_name_code_provider import StockInfoSzNameCodeProvider


class StockInfoSzNameCodeService(BaseService):
    """股票列表-深证服务"""
    
    collection_name = "stock_info_sz_name_code"
    provider_class = StockInfoSzNameCodeProvider
    
    # 时间字段名
    time_field = "更新时间"
