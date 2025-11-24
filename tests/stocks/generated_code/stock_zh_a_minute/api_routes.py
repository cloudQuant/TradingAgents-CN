
# 分时数据-新浪 - stock_zh_a_minute
@router.get("/collections/stock_zh_a_minute")
async def get_stock_zh_a_minute(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_minute/overview")
async def get_stock_zh_a_minute_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-新浪数据概览"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_minute/refresh")
async def refresh_stock_zh_a_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_minute/clear")
async def clear_stock_zh_a_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.clear_data()
