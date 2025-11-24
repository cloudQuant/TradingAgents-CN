
# 恒生指数股息率 - stock_hk_gxl_lg
@router.get("/collections/stock_hk_gxl_lg")
async def get_stock_hk_gxl_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_gxl_lg/overview")
async def get_stock_hk_gxl_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取恒生指数股息率数据概览"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_gxl_lg/refresh")
async def refresh_stock_hk_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_gxl_lg/clear")
async def clear_stock_hk_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.clear_data()
