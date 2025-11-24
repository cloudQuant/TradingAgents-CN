
# 北交所 - stock_register_bj
@router.get("/collections/stock_register_bj")
async def get_stock_register_bj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_bj/overview")
async def get_stock_register_bj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取北交所数据概览"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_bj/refresh")
async def refresh_stock_register_bj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_bj/clear")
async def clear_stock_register_bj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.clear_data()
