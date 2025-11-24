
# 板块详情 - stock_sector_detail
@router.get("/collections/stock_sector_detail")
async def get_stock_sector_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sector_detail/overview")
async def get_stock_sector_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块详情数据概览"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_sector_detail/refresh")
async def refresh_stock_sector_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sector_detail/clear")
async def clear_stock_sector_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.clear_data()
