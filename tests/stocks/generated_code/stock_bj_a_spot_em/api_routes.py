
# 京 A 股 - stock_bj_a_spot_em
@router.get("/collections/stock_bj_a_spot_em")
async def get_stock_bj_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_bj_a_spot_em/overview")
async def get_stock_bj_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取京 A 股数据概览"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_bj_a_spot_em/refresh")
async def refresh_stock_bj_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_bj_a_spot_em/clear")
async def clear_stock_bj_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.clear_data()
