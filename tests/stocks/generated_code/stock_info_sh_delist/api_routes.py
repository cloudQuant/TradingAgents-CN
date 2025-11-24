
# 暂停-终止上市-上证 - stock_info_sh_delist
@router.get("/collections/stock_info_sh_delist")
async def get_stock_info_sh_delist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sh_delist/overview")
async def get_stock_info_sh_delist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取暂停-终止上市-上证数据概览"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sh_delist/refresh")
async def refresh_stock_info_sh_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sh_delist/clear")
async def clear_stock_info_sh_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.clear_data()
