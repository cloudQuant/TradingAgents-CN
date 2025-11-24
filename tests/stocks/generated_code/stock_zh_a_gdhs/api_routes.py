
# 股东户数 - stock_zh_a_gdhs
@router.get("/collections/stock_zh_a_gdhs")
async def get_stock_zh_a_gdhs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_gdhs/overview")
async def get_stock_zh_a_gdhs_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数数据概览"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_gdhs/refresh")
async def refresh_stock_zh_a_gdhs(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_gdhs/clear")
async def clear_stock_zh_a_gdhs(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.clear_data()
