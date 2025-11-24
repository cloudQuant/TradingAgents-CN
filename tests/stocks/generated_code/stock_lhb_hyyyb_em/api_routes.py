
# 每日活跃营业部 - stock_lhb_hyyyb_em
@router.get("/collections/stock_lhb_hyyyb_em")
async def get_stock_lhb_hyyyb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_hyyyb_em/overview")
async def get_stock_lhb_hyyyb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取每日活跃营业部数据概览"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_hyyyb_em/refresh")
async def refresh_stock_lhb_hyyyb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_hyyyb_em/clear")
async def clear_stock_lhb_hyyyb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.clear_data()
