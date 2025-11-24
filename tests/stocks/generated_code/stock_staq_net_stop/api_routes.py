
# 两网及退市 - stock_staq_net_stop
@router.get("/collections/stock_staq_net_stop")
async def get_stock_staq_net_stop(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_staq_net_stop/overview")
async def get_stock_staq_net_stop_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据概览"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.get_overview()


@router.post("/collections/stock_staq_net_stop/refresh")
async def refresh_stock_staq_net_stop(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_staq_net_stop/clear")
async def clear_stock_staq_net_stop(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.clear_data()
