
# 上市公司质押比例 - stock_gpzy_pledge_ratio_em
@router.get("/collections/stock_gpzy_pledge_ratio_em")
async def get_stock_gpzy_pledge_ratio_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_pledge_ratio_em/overview")
async def get_stock_gpzy_pledge_ratio_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据概览"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_pledge_ratio_em/refresh")
async def refresh_stock_gpzy_pledge_ratio_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_pledge_ratio_em/clear")
async def clear_stock_gpzy_pledge_ratio_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.clear_data()
