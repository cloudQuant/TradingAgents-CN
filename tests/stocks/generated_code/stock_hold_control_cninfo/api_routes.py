
# 实际控制人持股变动 - stock_hold_control_cninfo
@router.get("/collections/stock_hold_control_cninfo")
async def get_stock_hold_control_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_control_cninfo/overview")
async def get_stock_hold_control_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实际控制人持股变动数据概览"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_control_cninfo/refresh")
async def refresh_stock_hold_control_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_control_cninfo/clear")
async def clear_stock_hold_control_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.clear_data()
