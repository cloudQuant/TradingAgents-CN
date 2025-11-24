
# 互动易-提问 - stock_irm_cninfo
@router.get("/collections/stock_irm_cninfo")
async def get_stock_irm_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_irm_cninfo/overview")
async def get_stock_irm_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-提问数据概览"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_irm_cninfo/refresh")
async def refresh_stock_irm_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_irm_cninfo/clear")
async def clear_stock_irm_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.clear_data()
