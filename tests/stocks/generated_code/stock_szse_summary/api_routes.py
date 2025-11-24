
# 证券类别统计 - stock_szse_summary
@router.get("/collections/stock_szse_summary")
async def get_stock_szse_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_summary/overview")
async def get_stock_szse_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券类别统计数据概览"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_summary/refresh")
async def refresh_stock_szse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_summary/clear")
async def clear_stock_szse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.clear_data()
