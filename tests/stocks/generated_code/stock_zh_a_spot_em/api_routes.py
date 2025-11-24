
# 沪深京A股实时行情-东财 - stock_zh_a_spot_em
@router.get("/collections/stock_zh_a_spot_em")
async def get_stock_zh_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_spot_em/overview")
async def get_stock_zh_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深京A股实时行情-东财数据概览"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_spot_em/refresh")
async def refresh_stock_zh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_spot_em/clear")
async def clear_stock_zh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.clear_data()
