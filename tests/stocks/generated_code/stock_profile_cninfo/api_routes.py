
# 公司概况-巨潮资讯 - stock_profile_cninfo
@router.get("/collections/stock_profile_cninfo")
async def get_stock_profile_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profile_cninfo/overview")
async def get_stock_profile_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司概况-巨潮资讯数据概览"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_profile_cninfo/refresh")
async def refresh_stock_profile_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profile_cninfo/clear")
async def clear_stock_profile_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.clear_data()
