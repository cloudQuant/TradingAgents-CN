
# 深圳主板 - stock_register_sz
@router.get("/collections/stock_register_sz")
async def get_stock_register_sz(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_sz/overview")
async def get_stock_register_sz_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深圳主板数据概览"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_sz/refresh")
async def refresh_stock_register_sz(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_sz/clear")
async def clear_stock_register_sz(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.clear_data()
