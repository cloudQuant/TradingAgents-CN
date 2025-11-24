
# 财报发行 - news_report_time_baidu
@router.get("/collections/news_report_time_baidu")
async def get_news_report_time_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_report_time_baidu/overview")
async def get_news_report_time_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据概览"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_report_time_baidu/refresh")
async def refresh_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_report_time_baidu/clear")
async def clear_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.clear_data()
