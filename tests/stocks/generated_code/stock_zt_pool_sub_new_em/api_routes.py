
# 次新股池 - stock_zt_pool_sub_new_em
@router.get("/collections/stock_zt_pool_sub_new_em")
async def get_stock_zt_pool_sub_new_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_sub_new_em/overview")
async def get_stock_zt_pool_sub_new_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取次新股池数据概览"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_sub_new_em/refresh")
async def refresh_stock_zt_pool_sub_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_sub_new_em/clear")
async def clear_stock_zt_pool_sub_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.clear_data()
