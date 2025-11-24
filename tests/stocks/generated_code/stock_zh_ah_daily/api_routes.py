
# 历史行情数据 - stock_zh_ah_daily
@router.get("/collections/stock_zh_ah_daily")
async def get_stock_zh_ah_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_daily/overview")
async def get_stock_zh_ah_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据概览"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_daily/refresh")
async def refresh_stock_zh_ah_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_daily/clear")
async def clear_stock_zh_ah_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.clear_data()
