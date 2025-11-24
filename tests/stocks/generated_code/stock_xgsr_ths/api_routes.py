
# 新股上市首日 - stock_xgsr_ths
@router.get("/collections/stock_xgsr_ths")
async def get_stock_xgsr_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_xgsr_ths/overview")
async def get_stock_xgsr_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股上市首日数据概览"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_xgsr_ths/refresh")
async def refresh_stock_xgsr_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_xgsr_ths/clear")
async def clear_stock_xgsr_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.clear_data()
