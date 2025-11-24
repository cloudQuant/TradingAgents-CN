
# 历史行情数据-腾讯 - stock_zh_a_hist_tx
@router.get("/collections/stock_zh_a_hist_tx")
async def get_stock_zh_a_hist_tx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist_tx/overview")
async def get_stock_zh_a_hist_tx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-腾讯数据概览"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist_tx/refresh")
async def refresh_stock_zh_a_hist_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist_tx/clear")
async def clear_stock_zh_a_hist_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.clear_data()
