
# 活跃营业部统计 - stock_dzjy_hyyybtj
@router.get("/collections/stock_dzjy_hyyybtj")
async def get_stock_dzjy_hyyybtj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_hyyybtj/overview")
async def get_stock_dzjy_hyyybtj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃营业部统计数据概览"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_hyyybtj/refresh")
async def refresh_stock_dzjy_hyyybtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_hyyybtj/clear")
async def clear_stock_dzjy_hyyybtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.clear_data()
