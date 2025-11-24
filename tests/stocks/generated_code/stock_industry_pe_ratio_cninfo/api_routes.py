
# 行业市盈率 - stock_industry_pe_ratio_cninfo
@router.get("/collections/stock_industry_pe_ratio_cninfo")
async def get_stock_industry_pe_ratio_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_pe_ratio_cninfo/overview")
async def get_stock_industry_pe_ratio_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业市盈率数据概览"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_pe_ratio_cninfo/refresh")
async def refresh_stock_industry_pe_ratio_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_pe_ratio_cninfo/clear")
async def clear_stock_industry_pe_ratio_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.clear_data()
