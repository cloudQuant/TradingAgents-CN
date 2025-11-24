
# 实时行情数据 - stock_zh_kcb_spot
@router.get("/collections/stock_zh_kcb_spot")
async def get_stock_zh_kcb_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_kcb_spot/overview")
async def get_stock_zh_kcb_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据数据概览"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_kcb_spot/refresh")
async def refresh_stock_zh_kcb_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_kcb_spot/clear")
async def clear_stock_zh_kcb_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.clear_data()
