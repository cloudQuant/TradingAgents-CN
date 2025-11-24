
# 分时数据 - stock_zh_b_minute
@router.get("/collections/stock_zh_b_minute")
async def get_stock_zh_b_minute(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_b_minute/overview")
async def get_stock_zh_b_minute_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据数据概览"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_b_minute/refresh")
async def refresh_stock_zh_b_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_b_minute/clear")
async def clear_stock_zh_b_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.clear_data()
