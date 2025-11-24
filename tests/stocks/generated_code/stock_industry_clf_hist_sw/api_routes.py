
# 申万个股行业分类变动历史 - stock_industry_clf_hist_sw
@router.get("/collections/stock_industry_clf_hist_sw")
async def get_stock_industry_clf_hist_sw(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_clf_hist_sw/overview")
async def get_stock_industry_clf_hist_sw_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取申万个股行业分类变动历史数据概览"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_clf_hist_sw/refresh")
async def refresh_stock_industry_clf_hist_sw(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_clf_hist_sw/clear")
async def clear_stock_industry_clf_hist_sw(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.clear_data()
