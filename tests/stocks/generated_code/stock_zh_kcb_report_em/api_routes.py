
# 科创板公告 - stock_zh_kcb_report_em
@router.get("/collections/stock_zh_kcb_report_em")
async def get_stock_zh_kcb_report_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_kcb_report_em/overview")
async def get_stock_zh_kcb_report_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板公告数据概览"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_kcb_report_em/refresh")
async def refresh_stock_zh_kcb_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_kcb_report_em/clear")
async def clear_stock_zh_kcb_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.clear_data()
