
# 上海证券交易所 - stock_sse_summary
@router.get("/collections/stock_sse_summary")
async def get_stock_sse_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sse_summary/overview")
async def get_stock_sse_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所数据概览"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_sse_summary/refresh")
async def refresh_stock_sse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sse_summary/clear")
async def clear_stock_sse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.clear_data()
