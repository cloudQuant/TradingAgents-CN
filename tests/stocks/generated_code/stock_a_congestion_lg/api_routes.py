
# 大盘拥挤度 - stock_a_congestion_lg
@router.get("/collections/stock_a_congestion_lg")
async def get_stock_a_congestion_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_congestion_lg/overview")
async def get_stock_a_congestion_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取大盘拥挤度数据概览"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_congestion_lg/refresh")
async def refresh_stock_a_congestion_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_congestion_lg/clear")
async def clear_stock_a_congestion_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.clear_data()
