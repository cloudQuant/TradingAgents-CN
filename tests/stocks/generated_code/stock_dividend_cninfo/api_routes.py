
# 历史分红 - stock_dividend_cninfo
@router.get("/collections/stock_dividend_cninfo")
async def get_stock_dividend_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dividend_cninfo/overview")
async def get_stock_dividend_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史分红数据概览"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_dividend_cninfo/refresh")
async def refresh_stock_dividend_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dividend_cninfo/clear")
async def clear_stock_dividend_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.clear_data()
