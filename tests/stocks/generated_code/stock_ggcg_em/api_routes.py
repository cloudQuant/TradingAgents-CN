
# 股东增减持 - stock_ggcg_em
@router.get("/collections/stock_ggcg_em")
async def get_stock_ggcg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ggcg_em/overview")
async def get_stock_ggcg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东增减持数据概览"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_ggcg_em/refresh")
async def refresh_stock_ggcg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ggcg_em/clear")
async def clear_stock_ggcg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.clear_data()
