
# 分红派息 - news_trade_notify_dividend_baidu
@router.get("/collections/news_trade_notify_dividend_baidu")
async def get_news_trade_notify_dividend_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_trade_notify_dividend_baidu/overview")
async def get_news_trade_notify_dividend_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据概览"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_trade_notify_dividend_baidu/refresh")
async def refresh_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_trade_notify_dividend_baidu/clear")
async def clear_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.clear_data()
