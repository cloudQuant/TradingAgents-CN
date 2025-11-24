
# 股票回购数据 - stock_repurchase_em
@router.get("/collections/stock_repurchase_em")
async def get_stock_repurchase_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_repurchase_em/overview")
async def get_stock_repurchase_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票回购数据数据概览"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_repurchase_em/refresh")
async def refresh_stock_repurchase_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_repurchase_em/clear")
async def clear_stock_repurchase_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.clear_data()
