
# 沪深港通资金流向 - stock_hsgt_fund_flow_summary_em
@router.get("/collections/stock_hsgt_fund_flow_summary_em")
async def get_stock_hsgt_fund_flow_summary_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hsgt_fund_flow_summary_em/overview")
async def get_stock_hsgt_fund_flow_summary_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深港通资金流向数据概览"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hsgt_fund_flow_summary_em/refresh")
async def refresh_stock_hsgt_fund_flow_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hsgt_fund_flow_summary_em/clear")
async def clear_stock_hsgt_fund_flow_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.clear_data()
