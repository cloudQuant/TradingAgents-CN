
# 达标企业 - stock_register_db
@router.get("/collections/stock_register_db")
async def get_stock_register_db(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_db/overview")
async def get_stock_register_db_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取达标企业数据概览"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_db/refresh")
async def refresh_stock_register_db(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_db/clear")
async def clear_stock_register_db(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.clear_data()
