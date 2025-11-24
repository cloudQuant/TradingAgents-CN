
# 风险警示板 - stock_zh_a_st_em
@router.get("/collections/stock_zh_a_st_em")
async def get_stock_zh_a_st_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_st_em/overview")
async def get_stock_zh_a_st_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取风险警示板数据概览"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_st_em/refresh")
async def refresh_stock_zh_a_st_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_st_em/clear")
async def clear_stock_zh_a_st_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.clear_data()
