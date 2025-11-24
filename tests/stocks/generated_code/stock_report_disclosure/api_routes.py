
# 预约披露时间-巨潮资讯 - stock_report_disclosure
@router.get("/collections/stock_report_disclosure")
async def get_stock_report_disclosure(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_disclosure/overview")
async def get_stock_report_disclosure_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取预约披露时间-巨潮资讯数据概览"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_disclosure/refresh")
async def refresh_stock_report_disclosure(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_disclosure/clear")
async def clear_stock_report_disclosure(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.clear_data()
