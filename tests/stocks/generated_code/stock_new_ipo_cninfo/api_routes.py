
# 新股发行 - stock_new_ipo_cninfo
@router.get("/collections/stock_new_ipo_cninfo")
async def get_stock_new_ipo_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_new_ipo_cninfo/overview")
async def get_stock_new_ipo_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股发行数据概览"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_new_ipo_cninfo/refresh")
async def refresh_stock_new_ipo_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_new_ipo_cninfo/clear")
async def clear_stock_new_ipo_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.clear_data()
