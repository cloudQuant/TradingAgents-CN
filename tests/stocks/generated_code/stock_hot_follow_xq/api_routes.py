
# 关注排行榜 - stock_hot_follow_xq
@router.get("/collections/stock_hot_follow_xq")
async def get_stock_hot_follow_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_follow_xq/overview")
async def get_stock_hot_follow_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取关注排行榜数据概览"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_follow_xq/refresh")
async def refresh_stock_hot_follow_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_follow_xq/clear")
async def clear_stock_hot_follow_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.clear_data()
