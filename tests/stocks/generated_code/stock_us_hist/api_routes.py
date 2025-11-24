
# 历史行情数据-东财 - stock_us_hist
@router.get("/collections/stock_us_hist")
async def get_stock_us_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_hist/overview")
async def get_stock_us_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据概览"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_hist/refresh")
async def refresh_stock_us_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_hist/clear")
async def clear_stock_us_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.clear_data()
