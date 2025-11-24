
# 人员增减持股变动明细 - stock_hold_management_person_em
@router.get("/collections/stock_hold_management_person_em")
async def get_stock_hold_management_person_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_person_em/overview")
async def get_stock_hold_management_person_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人员增减持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_person_em/refresh")
async def refresh_stock_hold_management_person_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_person_em/clear")
async def clear_stock_hold_management_person_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.clear_data()
