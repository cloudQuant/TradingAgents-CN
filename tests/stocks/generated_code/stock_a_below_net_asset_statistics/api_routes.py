
# 破净股统计 - stock_a_below_net_asset_statistics
@router.get("/collections/stock_a_below_net_asset_statistics")
async def get_stock_a_below_net_asset_statistics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_below_net_asset_statistics/overview")
async def get_stock_a_below_net_asset_statistics_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取破净股统计数据概览"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_below_net_asset_statistics/refresh")
async def refresh_stock_a_below_net_asset_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_below_net_asset_statistics/clear")
async def clear_stock_a_below_net_asset_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.clear_data()
