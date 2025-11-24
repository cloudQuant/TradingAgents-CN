
# 向上突破 - stock_rank_xstp_ths
@router.get("/collections/stock_rank_xstp_ths")
async def get_stock_rank_xstp_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_xstp_ths/overview")
async def get_stock_rank_xstp_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向上突破数据概览"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_xstp_ths/refresh")
async def refresh_stock_rank_xstp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_xstp_ths/clear")
async def clear_stock_rank_xstp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.clear_data()
