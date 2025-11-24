
# 腾讯财经 - stock_zh_a_tick_tx
@router.get("/collections/stock_zh_a_tick_tx")
async def get_stock_zh_a_tick_tx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_tick_tx/overview")
async def get_stock_zh_a_tick_tx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取腾讯财经数据概览"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_tick_tx/refresh")
async def refresh_stock_zh_a_tick_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_tick_tx/clear")
async def clear_stock_zh_a_tick_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.clear_data()
