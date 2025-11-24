
# 持续缩量 - stock_rank_cxsl_ths
@router.get("/collections/stock_rank_cxsl_ths")
async def get_stock_rank_cxsl_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_cxsl_ths/overview")
async def get_stock_rank_cxsl_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续缩量数据概览"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_cxsl_ths/refresh")
async def refresh_stock_rank_cxsl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_cxsl_ths/clear")
async def clear_stock_rank_cxsl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.clear_data()
