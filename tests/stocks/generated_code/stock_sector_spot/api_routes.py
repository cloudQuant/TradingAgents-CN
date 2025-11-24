
# 板块行情 - stock_sector_spot
@router.get("/collections/stock_sector_spot")
async def get_stock_sector_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sector_spot/overview")
async def get_stock_sector_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块行情数据概览"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_sector_spot/refresh")
async def refresh_stock_sector_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sector_spot/clear")
async def clear_stock_sector_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.clear_data()
