
# 盈利预测-同花顺 - stock_profit_forecast_ths
@router.get("/collections/stock_profit_forecast_ths")
async def get_stock_profit_forecast_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_forecast_ths/overview")
async def get_stock_profit_forecast_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-同花顺数据概览"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_forecast_ths/refresh")
async def refresh_stock_profit_forecast_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_forecast_ths/clear")
async def clear_stock_profit_forecast_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.clear_data()
