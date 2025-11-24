
# 首发申报信息 - stock_ipo_declare
@router.get("/collections/stock_ipo_declare")
async def get_stock_ipo_declare(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_declare/overview")
async def get_stock_ipo_declare_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取首发申报信息数据概览"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_declare/refresh")
async def refresh_stock_ipo_declare(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_declare/clear")
async def clear_stock_ipo_declare(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.clear_data()
