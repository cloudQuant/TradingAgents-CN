
# 巴菲特指标 - stock_buffett_index_lg
@router.get("/collections/stock_buffett_index_lg")
async def get_stock_buffett_index_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_buffett_index_lg/overview")
async def get_stock_buffett_index_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取巴菲特指标数据概览"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_buffett_index_lg/refresh")
async def refresh_stock_buffett_index_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_buffett_index_lg/clear")
async def clear_stock_buffett_index_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.clear_data()
