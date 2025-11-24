
# 财经内容精选 - stock_news_main_cx
@router.get("/collections/stock_news_main_cx")
async def get_stock_news_main_cx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_news_main_cx/overview")
async def get_stock_news_main_cx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财经内容精选数据概览"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.get_overview()


@router.post("/collections/stock_news_main_cx/refresh")
async def refresh_stock_news_main_cx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_news_main_cx/clear")
async def clear_stock_news_main_cx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.clear_data()
