
# 上海证券交易所-每日概况 - stock_sse_deal_daily
@router.get("/collections/stock_sse_deal_daily")
async def get_stock_sse_deal_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sse_deal_daily/overview")
async def get_stock_sse_deal_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所-每日概况数据概览"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_sse_deal_daily/refresh")
async def refresh_stock_sse_deal_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sse_deal_daily/clear")
async def clear_stock_sse_deal_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.clear_data()
