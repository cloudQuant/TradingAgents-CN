
# 流通股东 - stock_circulate_stock_holder
@router.get("/collections/stock_circulate_stock_holder")
async def get_stock_circulate_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_circulate_stock_holder/overview")
async def get_stock_circulate_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取流通股东数据概览"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_circulate_stock_holder/refresh")
async def refresh_stock_circulate_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_circulate_stock_holder/clear")
async def clear_stock_circulate_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.clear_data()
