
# 上市相关-巨潮资讯 - stock_ipo_summary_cninfo
@router.get("/collections/stock_ipo_summary_cninfo")
async def get_stock_ipo_summary_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_summary_cninfo/overview")
async def get_stock_ipo_summary_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市相关-巨潮资讯数据概览"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_summary_cninfo/refresh")
async def refresh_stock_ipo_summary_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_summary_cninfo/clear")
async def clear_stock_ipo_summary_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.clear_data()
