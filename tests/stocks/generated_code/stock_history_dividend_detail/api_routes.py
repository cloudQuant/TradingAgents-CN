
# 分红配股 - stock_history_dividend_detail
@router.get("/collections/stock_history_dividend_detail")
async def get_stock_history_dividend_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_history_dividend_detail/overview")
async def get_stock_history_dividend_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配股数据概览"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_history_dividend_detail/refresh")
async def refresh_stock_history_dividend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_history_dividend_detail/clear")
async def clear_stock_history_dividend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.clear_data()
