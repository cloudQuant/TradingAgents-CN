
# 配股实施方案-巨潮资讯 - stock_allotment_cninfo
@router.get("/collections/stock_allotment_cninfo")
async def get_stock_allotment_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_allotment_cninfo/overview")
async def get_stock_allotment_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股实施方案-巨潮资讯数据概览"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_allotment_cninfo/refresh")
async def refresh_stock_allotment_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_allotment_cninfo/clear")
async def clear_stock_allotment_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.clear_data()
