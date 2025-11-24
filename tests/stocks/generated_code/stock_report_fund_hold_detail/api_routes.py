
# 基金持股明细 - stock_report_fund_hold_detail
@router.get("/collections/stock_report_fund_hold_detail")
async def get_stock_report_fund_hold_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_fund_hold_detail/overview")
async def get_stock_report_fund_hold_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股明细数据概览"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_fund_hold_detail/refresh")
async def refresh_stock_report_fund_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_fund_hold_detail/clear")
async def clear_stock_report_fund_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.clear_data()
