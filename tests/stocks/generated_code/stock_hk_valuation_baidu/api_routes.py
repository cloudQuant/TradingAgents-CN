
# 港股估值指标 - stock_hk_valuation_baidu
@router.get("/collections/stock_hk_valuation_baidu")
async def get_stock_hk_valuation_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_valuation_baidu/overview")
async def get_stock_hk_valuation_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股估值指标数据概览"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_valuation_baidu/refresh")
async def refresh_stock_hk_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_valuation_baidu/clear")
async def clear_stock_hk_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.clear_data()
