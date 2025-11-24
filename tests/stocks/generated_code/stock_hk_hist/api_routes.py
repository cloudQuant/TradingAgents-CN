
# 历史行情数据-东财 - stock_hk_hist
@router.get("/collections/stock_hk_hist")
async def get_stock_hk_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hist/overview")
async def get_stock_hk_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据概览"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hist/refresh")
async def refresh_stock_hk_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hist/clear")
async def clear_stock_hk_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.clear_data()
