
# 个股限售解禁-新浪 - stock_restricted_release_queue_sina
@router.get("/collections/stock_restricted_release_queue_sina")
async def get_stock_restricted_release_queue_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_queue_sina/overview")
async def get_stock_restricted_release_queue_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股限售解禁-新浪数据概览"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_queue_sina/refresh")
async def refresh_stock_restricted_release_queue_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_queue_sina/clear")
async def clear_stock_restricted_release_queue_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.clear_data()
