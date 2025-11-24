
# 股权质押 - stock_cg_equity_mortgage_cninfo
@router.get("/collections/stock_cg_equity_mortgage_cninfo")
async def get_stock_cg_equity_mortgage_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_equity_mortgage_cninfo/overview")
async def get_stock_cg_equity_mortgage_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股权质押数据概览"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_equity_mortgage_cninfo/refresh")
async def refresh_stock_cg_equity_mortgage_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_equity_mortgage_cninfo/clear")
async def clear_stock_cg_equity_mortgage_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.clear_data()
