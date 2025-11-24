
# 董监高及相关人员持股变动-上证 - stock_share_hold_change_sse
@router.get("/collections/stock_share_hold_change_sse")
async def get_stock_share_hold_change_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_hold_change_sse/overview")
async def get_stock_share_hold_change_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-上证数据概览"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_hold_change_sse/refresh")
async def refresh_stock_share_hold_change_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_hold_change_sse/clear")
async def clear_stock_share_hold_change_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.clear_data()
