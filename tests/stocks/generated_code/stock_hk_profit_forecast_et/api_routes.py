
# 港股盈利预测-经济通 - stock_hk_profit_forecast_et
@router.get("/collections/stock_hk_profit_forecast_et")
async def get_stock_hk_profit_forecast_et(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_profit_forecast_et/overview")
async def get_stock_hk_profit_forecast_et_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股盈利预测-经济通数据概览"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_profit_forecast_et/refresh")
async def refresh_stock_hk_profit_forecast_et(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_profit_forecast_et/clear")
async def clear_stock_hk_profit_forecast_et(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.clear_data()
