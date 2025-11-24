
# A 股等权重与中位数市净率 - stock_a_all_pb
@router.get("/collections/stock_a_all_pb")
async def get_stock_a_all_pb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_all_pb/overview")
async def get_stock_a_all_pb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市净率数据概览"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_all_pb/refresh")
async def refresh_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_all_pb/clear")
async def clear_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.clear_data()
