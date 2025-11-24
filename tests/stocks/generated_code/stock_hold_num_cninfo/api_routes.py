
# 股东人数及持股集中度 - stock_hold_num_cninfo
@router.get("/collections/stock_hold_num_cninfo")
async def get_stock_hold_num_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_num_cninfo/overview")
async def get_stock_hold_num_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东人数及持股集中度数据概览"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_num_cninfo/refresh")
async def refresh_stock_hold_num_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_num_cninfo/clear")
async def clear_stock_hold_num_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.clear_data()
