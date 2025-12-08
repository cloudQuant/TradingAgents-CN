"""
大连商品交易所-持仓排名数据服务

支持增量更新：从数据库最大日期开始更新到今天
"""
from app.services.data_sources.futures.services.date_incremental_service import DateIncrementalService
from app.services.data_sources.futures.providers.futures_dce_position_rank_provider import FuturesDcePositionRankProvider


class FuturesDcePositionRankService(DateIncrementalService):
    """大连商品交易所-持仓排名数据服务"""
    
    collection_name = "futures_dce_position_rank"
    provider_class = FuturesDcePositionRankProvider
    
    time_field = "日期"
    unique_keys = ["日期", "品种", "会员名称", "排名"]
    DEFAULT_START_DATE = "20000101"  # 大商所数据从2000年开始
