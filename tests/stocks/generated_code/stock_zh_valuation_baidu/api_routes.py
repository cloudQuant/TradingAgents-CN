
# A 股估值指标 - stock_zh_valuation_baidu
@router.get("/collections/stock_zh_valuation_baidu")
async def get_stock_zh_valuation_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_valuation_baidu/overview")
async def get_stock_zh_valuation_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股估值指标数据概览"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_valuation_baidu/refresh")
async def refresh_stock_zh_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_valuation_baidu/clear")
async def clear_stock_zh_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.clear_data()
