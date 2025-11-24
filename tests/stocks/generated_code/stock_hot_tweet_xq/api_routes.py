
# 讨论排行榜 - stock_hot_tweet_xq
@router.get("/collections/stock_hot_tweet_xq")
async def get_stock_hot_tweet_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_tweet_xq/overview")
async def get_stock_hot_tweet_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取讨论排行榜数据概览"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_tweet_xq/refresh")
async def refresh_stock_hot_tweet_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_tweet_xq/clear")
async def clear_stock_hot_tweet_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.clear_data()
