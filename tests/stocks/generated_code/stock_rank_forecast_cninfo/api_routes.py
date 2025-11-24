
# 投资评级 - stock_rank_forecast_cninfo
@router.get("/collections/stock_rank_forecast_cninfo")
async def get_stock_rank_forecast_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_forecast_cninfo/overview")
async def get_stock_rank_forecast_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取投资评级数据概览"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_forecast_cninfo/refresh")
async def refresh_stock_rank_forecast_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_forecast_cninfo/clear")
async def clear_stock_rank_forecast_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.clear_data()
