
# 公司资料 - stock_hk_company_profile_em
@router.get("/collections/stock_hk_company_profile_em")
async def get_stock_hk_company_profile_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_company_profile_em/overview")
async def get_stock_hk_company_profile_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司资料数据概览"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_company_profile_em/refresh")
async def refresh_stock_hk_company_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_company_profile_em/clear")
async def clear_stock_hk_company_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.clear_data()
