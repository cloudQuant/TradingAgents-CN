
# 创新高和新低的股票数量 - stock_a_high_low_statistics
@router.get("/collections/stock_a_high_low_statistics")
async def get_stock_a_high_low_statistics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_high_low_statistics/overview")
async def get_stock_a_high_low_statistics_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创新高和新低的股票数量数据概览"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_high_low_statistics/refresh")
async def refresh_stock_a_high_low_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_high_low_statistics/clear")
async def clear_stock_a_high_low_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.clear_data()
