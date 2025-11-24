
# 实时行情数据-腾讯 - stock_zh_ah_spot
@router.get("/collections/stock_zh_ah_spot")
async def get_stock_zh_ah_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_spot/overview")
async def get_stock_zh_ah_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-腾讯数据概览"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_spot/refresh")
async def refresh_stock_zh_ah_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_spot/clear")
async def clear_stock_zh_ah_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.clear_data()
