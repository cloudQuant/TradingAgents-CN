
# 科创板 - stock_register_kcb
@router.get("/collections/stock_register_kcb")
async def get_stock_register_kcb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_kcb/overview")
async def get_stock_register_kcb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据概览"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_kcb/refresh")
async def refresh_stock_register_kcb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_kcb/clear")
async def clear_stock_register_kcb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.clear_data()
