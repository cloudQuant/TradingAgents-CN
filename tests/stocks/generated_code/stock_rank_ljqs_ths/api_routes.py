
# 量价齐升 - stock_rank_ljqs_ths
@router.get("/collections/stock_rank_ljqs_ths")
async def get_stock_rank_ljqs_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_ljqs_ths/overview")
async def get_stock_rank_ljqs_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐升数据概览"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_ljqs_ths/refresh")
async def refresh_stock_rank_ljqs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_ljqs_ths/clear")
async def clear_stock_rank_ljqs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.clear_data()
