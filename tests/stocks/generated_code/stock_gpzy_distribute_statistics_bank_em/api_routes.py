
# 质押机构分布统计-银行 - stock_gpzy_distribute_statistics_bank_em
@router.get("/collections/stock_gpzy_distribute_statistics_bank_em")
async def get_stock_gpzy_distribute_statistics_bank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_distribute_statistics_bank_em/overview")
async def get_stock_gpzy_distribute_statistics_bank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-银行数据概览"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_distribute_statistics_bank_em/refresh")
async def refresh_stock_gpzy_distribute_statistics_bank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_distribute_statistics_bank_em/clear")
async def clear_stock_gpzy_distribute_statistics_bank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.clear_data()
