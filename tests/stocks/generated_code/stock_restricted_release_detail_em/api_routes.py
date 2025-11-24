
# 限售股解禁详情 - stock_restricted_release_detail_em
@router.get("/collections/stock_restricted_release_detail_em")
async def get_stock_restricted_release_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_detail_em/overview")
async def get_stock_restricted_release_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁详情数据概览"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_detail_em/refresh")
async def refresh_stock_restricted_release_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_detail_em/clear")
async def clear_stock_restricted_release_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.clear_data()
