
# 营业部统计 - stock_lhb_traderstatistic_em
@router.get("/collections/stock_lhb_traderstatistic_em")
async def get_stock_lhb_traderstatistic_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_traderstatistic_em/overview")
async def get_stock_lhb_traderstatistic_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部统计数据概览"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_traderstatistic_em/refresh")
async def refresh_stock_lhb_traderstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_traderstatistic_em/clear")
async def clear_stock_lhb_traderstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.clear_data()
