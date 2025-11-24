
# 分时数据-东财 - stock_us_hist_min_em
@router.get("/collections/stock_us_hist_min_em")
async def get_stock_us_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_hist_min_em/overview")
async def get_stock_us_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据概览"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_hist_min_em/refresh")
async def refresh_stock_us_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_hist_min_em/clear")
async def clear_stock_us_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.clear_data()
