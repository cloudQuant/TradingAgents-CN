
# 内部交易 - stock_inner_trade_xq
@router.get("/collections/stock_inner_trade_xq")
async def get_stock_inner_trade_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_inner_trade_xq/overview")
async def get_stock_inner_trade_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取内部交易数据概览"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_inner_trade_xq/refresh")
async def refresh_stock_inner_trade_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_inner_trade_xq/clear")
async def clear_stock_inner_trade_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.clear_data()
