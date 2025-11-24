
# 董监高及相关人员持股变动明细 - stock_hold_management_detail_em
@router.get("/collections/stock_hold_management_detail_em")
async def get_stock_hold_management_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_detail_em/overview")
async def get_stock_hold_management_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_detail_em/refresh")
async def refresh_stock_hold_management_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_detail_em/clear")
async def clear_stock_hold_management_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.clear_data()
