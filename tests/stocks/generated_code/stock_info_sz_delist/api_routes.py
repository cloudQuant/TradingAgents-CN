
# 终止-暂停上市-深证 - stock_info_sz_delist
@router.get("/collections/stock_info_sz_delist")
async def get_stock_info_sz_delist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sz_delist/overview")
async def get_stock_info_sz_delist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取终止-暂停上市-深证数据概览"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sz_delist/refresh")
async def refresh_stock_info_sz_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sz_delist/clear")
async def clear_stock_info_sz_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.clear_data()
