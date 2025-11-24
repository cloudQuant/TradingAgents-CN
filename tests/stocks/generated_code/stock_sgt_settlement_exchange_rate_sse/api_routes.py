
# 结算汇率-沪港通 - stock_sgt_settlement_exchange_rate_sse
@router.get("/collections/stock_sgt_settlement_exchange_rate_sse")
async def get_stock_sgt_settlement_exchange_rate_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sgt_settlement_exchange_rate_sse/overview")
async def get_stock_sgt_settlement_exchange_rate_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-沪港通数据概览"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_sgt_settlement_exchange_rate_sse/refresh")
async def refresh_stock_sgt_settlement_exchange_rate_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sgt_settlement_exchange_rate_sse/clear")
async def clear_stock_sgt_settlement_exchange_rate_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.clear_data()
