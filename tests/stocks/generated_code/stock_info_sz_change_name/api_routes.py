
# 名称变更-深证 - stock_info_sz_change_name
@router.get("/collections/stock_info_sz_change_name")
async def get_stock_info_sz_change_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sz_change_name/overview")
async def get_stock_info_sz_change_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取名称变更-深证数据概览"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sz_change_name/refresh")
async def refresh_stock_info_sz_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sz_change_name/clear")
async def clear_stock_info_sz_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.clear_data()
