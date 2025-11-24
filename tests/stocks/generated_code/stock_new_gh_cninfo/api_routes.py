
# 新股过会 - stock_new_gh_cninfo
@router.get("/collections/stock_new_gh_cninfo")
async def get_stock_new_gh_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_new_gh_cninfo/overview")
async def get_stock_new_gh_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股过会数据概览"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_new_gh_cninfo/refresh")
async def refresh_stock_new_gh_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_new_gh_cninfo/clear")
async def clear_stock_new_gh_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.clear_data()
