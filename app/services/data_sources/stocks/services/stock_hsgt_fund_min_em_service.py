"""
沪深港通分时数据服务

东方财富-数据中心-沪深港通-市场概括-分时数据
接口: stock_hsgt_fund_min_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_fund_min_em_provider import StockHsgtFundMinEmProvider


class StockHsgtFundMinEmService(BaseService):
    """沪深港通分时数据服务"""
    
    collection_name = "stock_hsgt_fund_min_em"
    provider_class = StockHsgtFundMinEmProvider
    
    # 时间字段名
    time_field = "更新时间"
