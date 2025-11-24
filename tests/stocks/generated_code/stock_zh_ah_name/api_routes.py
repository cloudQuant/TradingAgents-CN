
# A+H股票字典 - stock_zh_ah_name
@router.get("/collections/stock_zh_ah_name")
async def get_stock_zh_ah_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_name/overview")
async def get_stock_zh_ah_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A+H股票字典数据概览"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_name/refresh")
async def refresh_stock_zh_ah_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_name/clear")
async def clear_stock_zh_ah_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.clear_data()
