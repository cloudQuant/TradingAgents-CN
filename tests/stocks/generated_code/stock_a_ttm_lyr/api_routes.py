
# A 股等权重与中位数市盈率 - stock_a_ttm_lyr
@router.get("/collections/stock_a_ttm_lyr")
async def get_stock_a_ttm_lyr(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_ttm_lyr/overview")
async def get_stock_a_ttm_lyr_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市盈率数据概览"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_ttm_lyr/refresh")
async def refresh_stock_a_ttm_lyr(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_ttm_lyr/clear")
async def clear_stock_a_ttm_lyr(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.clear_data()
