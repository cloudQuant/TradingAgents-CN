
# 商誉减值预期明细 - stock_sy_yq_em
@router.get("/collections/stock_sy_yq_em")
async def get_stock_sy_yq_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_yq_em/overview")
async def get_stock_sy_yq_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取商誉减值预期明细数据概览"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_yq_em/refresh")
async def refresh_stock_sy_yq_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_yq_em/clear")
async def clear_stock_sy_yq_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.clear_data()
