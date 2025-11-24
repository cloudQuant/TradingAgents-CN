
# 上证e互动 - stock_sns_sseinfo
@router.get("/collections/stock_sns_sseinfo")
async def get_stock_sns_sseinfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sns_sseinfo/overview")
async def get_stock_sns_sseinfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上证e互动数据概览"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_sns_sseinfo/refresh")
async def refresh_stock_sns_sseinfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sns_sseinfo/clear")
async def clear_stock_sns_sseinfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.clear_data()
