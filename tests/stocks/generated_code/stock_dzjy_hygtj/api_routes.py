
# 活跃 A 股统计 - stock_dzjy_hygtj
@router.get("/collections/stock_dzjy_hygtj")
async def get_stock_dzjy_hygtj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_hygtj/overview")
async def get_stock_dzjy_hygtj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃 A 股统计数据概览"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_hygtj/refresh")
async def refresh_stock_dzjy_hygtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_hygtj/clear")
async def clear_stock_dzjy_hygtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.clear_data()
