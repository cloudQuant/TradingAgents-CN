
# 资产负债表-沪深 - stock_zcfz_em
@router.get("/collections/stock_zcfz_em")
async def get_stock_zcfz_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zcfz_em/overview")
async def get_stock_zcfz_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-沪深数据概览"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zcfz_em/refresh")
async def refresh_stock_zcfz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zcfz_em/clear")
async def clear_stock_zcfz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.clear_data()
