
# 日内分时数据-新浪 - stock_intraday_sina
@router.get("/collections/stock_intraday_sina")
async def get_stock_intraday_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_intraday_sina/overview")
async def get_stock_intraday_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-新浪数据概览"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_intraday_sina/refresh")
async def refresh_stock_intraday_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_intraday_sina/clear")
async def clear_stock_intraday_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.clear_data()
