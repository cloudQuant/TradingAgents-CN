
# 两网及退市 - stock_zh_a_stop_em
@router.get("/collections/stock_zh_a_stop_em")
async def get_stock_zh_a_stop_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_stop_em/overview")
async def get_stock_zh_a_stop_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据概览"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_stop_em/refresh")
async def refresh_stock_zh_a_stop_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_stop_em/clear")
async def clear_stock_zh_a_stop_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.clear_data()
