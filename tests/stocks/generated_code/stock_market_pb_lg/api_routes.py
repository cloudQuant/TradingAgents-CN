
# 主板市净率 - stock_market_pb_lg
@router.get("/collections/stock_market_pb_lg")
async def get_stock_market_pb_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_market_pb_lg/overview")
async def get_stock_market_pb_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市净率数据概览"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_market_pb_lg/refresh")
async def refresh_stock_market_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_market_pb_lg/clear")
async def clear_stock_market_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.clear_data()
