
# 基金持股 - stock_fund_stock_holder
@router.get("/collections/stock_fund_stock_holder")
async def get_stock_fund_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_fund_stock_holder/overview")
async def get_stock_fund_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据概览"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_fund_stock_holder/refresh")
async def refresh_stock_fund_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_fund_stock_holder/clear")
async def clear_stock_fund_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.clear_data()
