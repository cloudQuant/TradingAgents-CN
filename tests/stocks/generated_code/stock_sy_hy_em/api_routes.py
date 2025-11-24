
# 行业商誉 - stock_sy_hy_em
@router.get("/collections/stock_sy_hy_em")
async def get_stock_sy_hy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_hy_em/overview")
async def get_stock_sy_hy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业商誉数据概览"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_hy_em/refresh")
async def refresh_stock_sy_hy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_hy_em/clear")
async def clear_stock_sy_hy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.clear_data()
