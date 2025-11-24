
# 日内分时数据-东财 - stock_intraday_em
@router.get("/collections/stock_intraday_em")
async def get_stock_intraday_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_intraday_em/overview")
async def get_stock_intraday_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-东财数据概览"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_intraday_em/refresh")
async def refresh_stock_intraday_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_intraday_em/clear")
async def clear_stock_intraday_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.clear_data()
