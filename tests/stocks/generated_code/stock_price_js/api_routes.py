
# 美港目标价 - stock_price_js
@router.get("/collections/stock_price_js")
async def get_stock_price_js(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_price_js/overview")
async def get_stock_price_js_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取美港目标价数据概览"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.get_overview()


@router.post("/collections/stock_price_js/refresh")
async def refresh_stock_price_js(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_price_js/clear")
async def clear_stock_price_js(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.clear_data()
