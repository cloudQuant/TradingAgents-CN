
# 主营介绍-同花顺 - stock_zyjs_ths
@router.get("/collections/stock_zyjs_ths")
async def get_stock_zyjs_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zyjs_ths/overview")
async def get_stock_zyjs_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营介绍-同花顺数据概览"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_zyjs_ths/refresh")
async def refresh_stock_zyjs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zyjs_ths/clear")
async def clear_stock_zyjs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.clear_data()
