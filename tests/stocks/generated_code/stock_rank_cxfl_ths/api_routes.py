
# 持续放量 - stock_rank_cxfl_ths
@router.get("/collections/stock_rank_cxfl_ths")
async def get_stock_rank_cxfl_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_cxfl_ths/overview")
async def get_stock_rank_cxfl_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续放量数据概览"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_cxfl_ths/refresh")
async def refresh_stock_rank_cxfl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_cxfl_ths/clear")
async def clear_stock_rank_cxfl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.clear_data()
