
# 人气榜-A股 - stock_hot_rank_em
@router.get("/collections/stock_hot_rank_em")
async def get_stock_hot_rank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_em/overview")
async def get_stock_hot_rank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-A股数据概览"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_em/refresh")
async def refresh_stock_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_em/clear")
async def clear_stock_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.clear_data()
