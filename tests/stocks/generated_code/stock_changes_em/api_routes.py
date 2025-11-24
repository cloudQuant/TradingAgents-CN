
# 盘口异动 - stock_changes_em
@router.get("/collections/stock_changes_em")
async def get_stock_changes_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_changes_em/overview")
async def get_stock_changes_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘口异动数据概览"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_changes_em/refresh")
async def refresh_stock_changes_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_changes_em/clear")
async def clear_stock_changes_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.clear_data()
