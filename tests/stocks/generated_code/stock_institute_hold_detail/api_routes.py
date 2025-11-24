
# 机构持股详情 - stock_institute_hold_detail
@router.get("/collections/stock_institute_hold_detail")
async def get_stock_institute_hold_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_hold_detail/overview")
async def get_stock_institute_hold_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股详情数据概览"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_hold_detail/refresh")
async def refresh_stock_institute_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_hold_detail/clear")
async def clear_stock_institute_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.clear_data()
