
# 对外担保 - stock_cg_guarantee_cninfo
@router.get("/collections/stock_cg_guarantee_cninfo")
async def get_stock_cg_guarantee_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_guarantee_cninfo/overview")
async def get_stock_cg_guarantee_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取对外担保数据概览"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_guarantee_cninfo/refresh")
async def refresh_stock_cg_guarantee_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_guarantee_cninfo/clear")
async def clear_stock_cg_guarantee_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.clear_data()
