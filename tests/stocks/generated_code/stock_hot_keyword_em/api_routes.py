
# 热门关键词 - stock_hot_keyword_em
@router.get("/collections/stock_hot_keyword_em")
async def get_stock_hot_keyword_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_keyword_em/overview")
async def get_stock_hot_keyword_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热门关键词数据概览"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_keyword_em/refresh")
async def refresh_stock_hot_keyword_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_keyword_em/clear")
async def clear_stock_hot_keyword_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.clear_data()
