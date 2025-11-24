
# 机构席位追踪 - stock_lhb_jgstatistic_em
@router.get("/collections/stock_lhb_jgstatistic_em")
async def get_stock_lhb_jgstatistic_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgstatistic_em/overview")
async def get_stock_lhb_jgstatistic_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构席位追踪数据概览"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgstatistic_em/refresh")
async def refresh_stock_lhb_jgstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgstatistic_em/clear")
async def clear_stock_lhb_jgstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.clear_data()
