
# 股票增发 - stock_add_stock
@router.get("/collections/stock_add_stock")
async def get_stock_add_stock(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_add_stock/overview")
async def get_stock_add_stock_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票增发数据概览"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.get_overview()


@router.post("/collections/stock_add_stock/refresh")
async def refresh_stock_add_stock(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_add_stock/clear")
async def clear_stock_add_stock(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.clear_data()
