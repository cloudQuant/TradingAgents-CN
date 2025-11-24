
# 险资举牌 - stock_rank_xzjp_ths
@router.get("/collections/stock_rank_xzjp_ths")
async def get_stock_rank_xzjp_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_xzjp_ths/overview")
async def get_stock_rank_xzjp_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取险资举牌数据概览"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_xzjp_ths/refresh")
async def refresh_stock_rank_xzjp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_xzjp_ths/clear")
async def clear_stock_rank_xzjp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.clear_data()
