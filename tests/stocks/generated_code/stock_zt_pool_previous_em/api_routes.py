
# 昨日涨停股池 - stock_zt_pool_previous_em
@router.get("/collections/stock_zt_pool_previous_em")
async def get_stock_zt_pool_previous_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_previous_em/overview")
async def get_stock_zt_pool_previous_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取昨日涨停股池数据概览"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_previous_em/refresh")
async def refresh_stock_zt_pool_previous_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_previous_em/clear")
async def clear_stock_zt_pool_previous_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.clear_data()
