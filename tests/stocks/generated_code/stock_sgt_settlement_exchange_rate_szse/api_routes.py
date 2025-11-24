
# 结算汇率-深港通 - stock_sgt_settlement_exchange_rate_szse
@router.get("/collections/stock_sgt_settlement_exchange_rate_szse")
async def get_stock_sgt_settlement_exchange_rate_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sgt_settlement_exchange_rate_szse/overview")
async def get_stock_sgt_settlement_exchange_rate_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-深港通数据概览"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_sgt_settlement_exchange_rate_szse/refresh")
async def refresh_stock_sgt_settlement_exchange_rate_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sgt_settlement_exchange_rate_szse/clear")
async def clear_stock_sgt_settlement_exchange_rate_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.clear_data()
