
# 涨跌投票 - stock_zh_vote_baidu
@router.get("/collections/stock_zh_vote_baidu")
async def get_stock_zh_vote_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_vote_baidu/overview")
async def get_stock_zh_vote_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨跌投票数据概览"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_vote_baidu/refresh")
async def refresh_stock_zh_vote_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_vote_baidu/clear")
async def clear_stock_zh_vote_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.clear_data()
