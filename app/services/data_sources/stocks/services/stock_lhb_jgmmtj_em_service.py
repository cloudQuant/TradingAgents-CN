"""
机构买卖每日统计服务

东方财富网-数据中心-龙虎榜单-机构买卖每日统计
接口: stock_lhb_jgmmtj_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lhb_jgmmtj_em_provider import StockLhbJgmmtjEmProvider


class StockLhbJgmmtjEmService(BaseService):
    """机构买卖每日统计服务"""
    
    collection_name = "stock_lhb_jgmmtj_em"
    provider_class = StockLhbJgmmtjEmProvider
    
    # 时间字段名
    time_field = "更新时间"
