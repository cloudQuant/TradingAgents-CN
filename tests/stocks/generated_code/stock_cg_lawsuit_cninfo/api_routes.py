
# 公司诉讼 - stock_cg_lawsuit_cninfo
@router.get("/collections/stock_cg_lawsuit_cninfo")
async def get_stock_cg_lawsuit_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_lawsuit_cninfo/overview")
async def get_stock_cg_lawsuit_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司诉讼数据概览"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_lawsuit_cninfo/refresh")
async def refresh_stock_cg_lawsuit_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_lawsuit_cninfo/clear")
async def clear_stock_cg_lawsuit_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.clear_data()
