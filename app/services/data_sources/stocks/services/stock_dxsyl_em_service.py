"""
打新收益率服务

东方财富网-数据中心-新股申购-打新收益率
接口: stock_dxsyl_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_dxsyl_em_provider import StockDxsylEmProvider


class StockDxsylEmService(SimpleService):
    """打新收益率服务"""
    
    collection_name = "stock_dxsyl_em"
    provider_class = StockDxsylEmProvider
    
    # 时间字段名
    time_field = "更新时间"
