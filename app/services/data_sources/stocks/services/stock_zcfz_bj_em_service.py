"""
资产负债表-北交所服务

东方财富-数据中心-年报季报-业绩快报-资产负债表
接口: stock_zcfz_bj_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zcfz_bj_em_provider import StockZcfzBjEmProvider


class StockZcfzBjEmService(BaseService):
    """资产负债表-北交所服务"""
    
    collection_name = "stock_zcfz_bj_em"
    provider_class = StockZcfzBjEmProvider
    
    # 时间字段名
    time_field = "更新时间"
