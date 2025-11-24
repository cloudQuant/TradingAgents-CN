
# 财务指标 - stock_hk_financial_indicator_em
@router.get("/collections/stock_hk_financial_indicator_em")
async def get_stock_hk_financial_indicator_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_financial_indicator_em/overview")
async def get_stock_hk_financial_indicator_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财务指标数据概览"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_financial_indicator_em/refresh")
async def refresh_stock_hk_financial_indicator_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_financial_indicator_em/clear")
async def clear_stock_hk_financial_indicator_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.clear_data()
