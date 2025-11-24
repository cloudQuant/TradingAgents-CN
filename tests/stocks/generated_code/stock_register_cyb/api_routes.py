
# 创业板 - stock_register_cyb
@router.get("/collections/stock_register_cyb")
async def get_stock_register_cyb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_cyb/overview")
async def get_stock_register_cyb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据概览"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_cyb/refresh")
async def refresh_stock_register_cyb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_cyb/clear")
async def clear_stock_register_cyb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.clear_data()
