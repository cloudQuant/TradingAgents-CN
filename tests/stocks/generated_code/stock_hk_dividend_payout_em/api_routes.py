
# 分红派息 - stock_hk_dividend_payout_em
@router.get("/collections/stock_hk_dividend_payout_em")
async def get_stock_hk_dividend_payout_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_dividend_payout_em/overview")
async def get_stock_hk_dividend_payout_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据概览"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_dividend_payout_em/refresh")
async def refresh_stock_hk_dividend_payout_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_dividend_payout_em/clear")
async def clear_stock_hk_dividend_payout_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.clear_data()
