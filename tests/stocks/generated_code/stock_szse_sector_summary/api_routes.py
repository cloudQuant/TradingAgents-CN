
# 股票行业成交 - stock_szse_sector_summary
@router.get("/collections/stock_szse_sector_summary")
async def get_stock_szse_sector_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_sector_summary/overview")
async def get_stock_szse_sector_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票行业成交数据概览"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_sector_summary/refresh")
async def refresh_stock_szse_sector_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_sector_summary/clear")
async def clear_stock_szse_sector_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.clear_data()
