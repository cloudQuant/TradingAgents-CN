
# 机构持股一览表 - stock_institute_hold
@router.get("/collections/stock_institute_hold")
async def get_stock_institute_hold(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_hold/overview")
async def get_stock_institute_hold_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股一览表数据概览"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_hold/refresh")
async def refresh_stock_institute_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_hold/clear")
async def clear_stock_institute_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.clear_data()
