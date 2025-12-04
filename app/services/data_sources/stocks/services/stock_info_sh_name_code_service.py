"""
股票列表-上证服务

上海证券交易所股票代码和简称数据
接口: stock_info_sh_name_code
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_sh_name_code_provider import StockInfoShNameCodeProvider


class StockInfoShNameCodeService(BaseService):
    """股票列表-上证服务"""
    
    collection_name = "stock_info_sh_name_code"
    provider_class = StockInfoShNameCodeProvider
    
    # 时间字段名
    time_field = "更新时间"
