
# 个股商誉明细 - stock_sy_em
@router.get("/collections/stock_sy_em")
async def get_stock_sy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_em/overview")
async def get_stock_sy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉明细数据概览"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_em/refresh")
async def refresh_stock_sy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_em/clear")
async def clear_stock_sy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.clear_data()
