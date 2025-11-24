
# 高管持股变动明细 - stock_hold_management_detail_cninfo
@router.get("/collections/stock_hold_management_detail_cninfo")
async def get_stock_hold_management_detail_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_detail_cninfo/overview")
async def get_stock_hold_management_detail_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取高管持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_detail_cninfo/refresh")
async def refresh_stock_hold_management_detail_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_detail_cninfo/clear")
async def clear_stock_hold_management_detail_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.clear_data()
