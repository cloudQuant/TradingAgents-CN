
# 港股 - stock_hk_hot_rank_detail_realtime_em
@router.get("/collections/stock_hk_hot_rank_detail_realtime_em")
async def get_stock_hk_hot_rank_detail_realtime_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hot_rank_detail_realtime_em/overview")
async def get_stock_hk_hot_rank_detail_realtime_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据概览"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hot_rank_detail_realtime_em/refresh")
async def refresh_stock_hk_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hot_rank_detail_realtime_em/clear")
async def clear_stock_hk_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.clear_data()
