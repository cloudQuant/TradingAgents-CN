
# 历史行情数据-新浪 - stock_hk_daily
@router.get("/collections/stock_hk_daily")
async def get_stock_hk_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_daily/overview")
async def get_stock_hk_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据概览"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_daily/refresh")
async def refresh_stock_hk_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_daily/clear")
async def clear_stock_hk_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.clear_data()
