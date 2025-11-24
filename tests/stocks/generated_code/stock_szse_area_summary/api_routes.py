
# 地区交易排序 - stock_szse_area_summary
@router.get("/collections/stock_szse_area_summary")
async def get_stock_szse_area_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_area_summary/overview")
async def get_stock_szse_area_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取地区交易排序数据概览"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_area_summary/refresh")
async def refresh_stock_szse_area_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_area_summary/clear")
async def clear_stock_szse_area_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.clear_data()
