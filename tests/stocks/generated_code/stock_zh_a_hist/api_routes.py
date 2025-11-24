
# A股历史行情-东财 - stock_zh_a_hist
@router.get("/collections/stock_zh_a_hist")
async def get_stock_zh_a_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist/overview")
async def get_stock_zh_a_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股历史行情-东财数据概览"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist/refresh")
async def refresh_stock_zh_a_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist/clear")
async def clear_stock_zh_a_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.clear_data()
