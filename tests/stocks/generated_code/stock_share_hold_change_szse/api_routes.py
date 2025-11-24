
# 董监高及相关人员持股变动-深证 - stock_share_hold_change_szse
@router.get("/collections/stock_share_hold_change_szse")
async def get_stock_share_hold_change_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_hold_change_szse/overview")
async def get_stock_share_hold_change_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-深证数据概览"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_hold_change_szse/refresh")
async def refresh_stock_share_hold_change_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_hold_change_szse/clear")
async def clear_stock_share_hold_change_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.clear_data()
