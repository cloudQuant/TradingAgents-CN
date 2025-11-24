
# 业绩报表 - stock_yjbb_em
@router.get("/collections/stock_yjbb_em")
async def get_stock_yjbb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_yjbb_em/overview")
async def get_stock_yjbb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩报表数据概览"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_yjbb_em/refresh")
async def refresh_stock_yjbb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_yjbb_em/clear")
async def clear_stock_yjbb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.clear_data()
