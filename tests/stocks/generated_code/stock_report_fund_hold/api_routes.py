
# 基金持股 - stock_report_fund_hold
@router.get("/collections/stock_report_fund_hold")
async def get_stock_report_fund_hold(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_fund_hold/overview")
async def get_stock_report_fund_hold_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据概览"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_fund_hold/refresh")
async def refresh_stock_report_fund_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_fund_hold/clear")
async def clear_stock_report_fund_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.clear_data()
