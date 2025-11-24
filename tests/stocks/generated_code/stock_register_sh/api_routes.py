
# 上海主板 - stock_register_sh
@router.get("/collections/stock_register_sh")
async def get_stock_register_sh(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_sh/overview")
async def get_stock_register_sh_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海主板数据概览"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_sh/refresh")
async def refresh_stock_register_sh(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_sh/clear")
async def clear_stock_register_sh(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.clear_data()
