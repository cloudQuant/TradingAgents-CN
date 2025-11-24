
# 热搜股票 - stock_hot_search_baidu
@router.get("/collections/stock_hot_search_baidu")
async def get_stock_hot_search_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_search_baidu/overview")
async def get_stock_hot_search_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热搜股票数据概览"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_search_baidu/refresh")
async def refresh_stock_hot_search_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_search_baidu/clear")
async def clear_stock_hot_search_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.clear_data()
