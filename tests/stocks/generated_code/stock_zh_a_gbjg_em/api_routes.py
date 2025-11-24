
# 股本结构 - stock_zh_a_gbjg_em
@router.get("/collections/stock_zh_a_gbjg_em")
async def get_stock_zh_a_gbjg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_gbjg_em/overview")
async def get_stock_zh_a_gbjg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本结构数据概览"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_gbjg_em/refresh")
async def refresh_stock_zh_a_gbjg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_gbjg_em/clear")
async def clear_stock_zh_a_gbjg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.clear_data()
