
# 解禁股东 - stock_restricted_release_stockholder_em
@router.get("/collections/stock_restricted_release_stockholder_em")
async def get_stock_restricted_release_stockholder_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_stockholder_em/overview")
async def get_stock_restricted_release_stockholder_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取解禁股东数据概览"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_stockholder_em/refresh")
async def refresh_stock_restricted_release_stockholder_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_stockholder_em/clear")
async def clear_stock_restricted_release_stockholder_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.clear_data()
