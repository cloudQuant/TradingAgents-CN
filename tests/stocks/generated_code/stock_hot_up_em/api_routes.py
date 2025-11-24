
# 飙升榜-A股 - stock_hot_up_em
@router.get("/collections/stock_hot_up_em")
async def get_stock_hot_up_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_up_em/overview")
async def get_stock_hot_up_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取飙升榜-A股数据概览"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_up_em/refresh")
async def refresh_stock_hot_up_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_up_em/clear")
async def clear_stock_hot_up_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.clear_data()
