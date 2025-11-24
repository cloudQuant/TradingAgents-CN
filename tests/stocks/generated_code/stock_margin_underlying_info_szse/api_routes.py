
# 标的证券信息 - stock_margin_underlying_info_szse
@router.get("/collections/stock_margin_underlying_info_szse")
async def get_stock_margin_underlying_info_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_underlying_info_szse/overview")
async def get_stock_margin_underlying_info_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券信息数据概览"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_underlying_info_szse/refresh")
async def refresh_stock_margin_underlying_info_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_underlying_info_szse/clear")
async def clear_stock_margin_underlying_info_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.clear_data()
