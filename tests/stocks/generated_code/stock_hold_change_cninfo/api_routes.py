
# 股本变动 - stock_hold_change_cninfo
@router.get("/collections/stock_hold_change_cninfo")
async def get_stock_hold_change_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_change_cninfo/overview")
async def get_stock_hold_change_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本变动数据概览"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_change_cninfo/refresh")
async def refresh_stock_hold_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_change_cninfo/clear")
async def clear_stock_hold_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.clear_data()
