
# 公司股本变动-巨潮资讯 - stock_share_change_cninfo
@router.get("/collections/stock_share_change_cninfo")
async def get_stock_share_change_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_change_cninfo/overview")
async def get_stock_share_change_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司股本变动-巨潮资讯数据概览"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_change_cninfo/refresh")
async def refresh_stock_share_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_change_cninfo/clear")
async def clear_stock_share_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.clear_data()
