"""
沪深港通-港股通(沪>港)实时行情服务

东方财富网-行情中心-沪深港通-港股通(沪>港)-股票；按股票代码排序
接口: stock_hsgt_sh_hk_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hsgt_sh_hk_spot_em_provider import StockHsgtShHkSpotEmProvider


class StockHsgtShHkSpotEmService(SimpleService):
    """沪深港通-港股通(沪>港)实时行情服务"""
    
    collection_name = "stock_hsgt_sh_hk_spot_em"
    provider_class = StockHsgtShHkSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
