
# 配股 - stock_pg_em
@router.get("/collections/stock_pg_em")
async def get_stock_pg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_pg_em/overview")
async def get_stock_pg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股数据概览"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_pg_em/refresh")
async def refresh_stock_pg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_pg_em/clear")
async def clear_stock_pg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.clear_data()
