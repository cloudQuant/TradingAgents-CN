
# 估值比较 - stock_zh_valuation_comparison_em
@router.get("/collections/stock_zh_valuation_comparison_em")
async def get_stock_zh_valuation_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_valuation_comparison_em/overview")
async def get_stock_zh_valuation_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值比较数据概览"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_valuation_comparison_em/refresh")
async def refresh_stock_zh_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_valuation_comparison_em/clear")
async def clear_stock_zh_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.clear_data()
