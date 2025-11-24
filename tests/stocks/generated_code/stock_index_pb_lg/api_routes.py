
# 指数市净率 - stock_index_pb_lg
@router.get("/collections/stock_index_pb_lg")
async def get_stock_index_pb_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_index_pb_lg/overview")
async def get_stock_index_pb_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市净率数据概览"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_index_pb_lg/refresh")
async def refresh_stock_index_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_index_pb_lg/clear")
async def clear_stock_index_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.clear_data()
