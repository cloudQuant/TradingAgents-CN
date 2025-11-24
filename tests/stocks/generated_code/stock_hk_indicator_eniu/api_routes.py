
# 港股个股指标 - stock_hk_indicator_eniu
@router.get("/collections/stock_hk_indicator_eniu")
async def get_stock_hk_indicator_eniu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_indicator_eniu/overview")
async def get_stock_hk_indicator_eniu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股个股指标数据概览"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_indicator_eniu/refresh")
async def refresh_stock_hk_indicator_eniu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_indicator_eniu/clear")
async def clear_stock_hk_indicator_eniu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.clear_data()
