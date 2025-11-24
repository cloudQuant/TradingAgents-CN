
# 主要股东 - stock_main_stock_holder
@router.get("/collections/stock_main_stock_holder")
async def get_stock_main_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_main_stock_holder/overview")
async def get_stock_main_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主要股东数据概览"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_main_stock_holder/refresh")
async def refresh_stock_main_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_main_stock_holder/clear")
async def clear_stock_main_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.clear_data()
