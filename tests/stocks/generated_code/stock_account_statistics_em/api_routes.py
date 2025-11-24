
# 股票账户统计月度 - stock_account_statistics_em
@router.get("/collections/stock_account_statistics_em")
async def get_stock_account_statistics_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_account_statistics_em/overview")
async def get_stock_account_statistics_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票账户统计月度数据概览"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_account_statistics_em/refresh")
async def refresh_stock_account_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_account_statistics_em/clear")
async def clear_stock_account_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.clear_data()
