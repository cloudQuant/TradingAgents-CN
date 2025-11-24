
# 盈利预测-东方财富 - stock_profit_forecast_em
@router.get("/collections/stock_profit_forecast_em")
async def get_stock_profit_forecast_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_forecast_em/overview")
async def get_stock_profit_forecast_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-东方财富数据概览"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_forecast_em/refresh")
async def refresh_stock_profit_forecast_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_forecast_em/clear")
async def clear_stock_profit_forecast_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.clear_data()
