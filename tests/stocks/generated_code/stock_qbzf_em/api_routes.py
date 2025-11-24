
# 增发 - stock_qbzf_em
@router.get("/collections/stock_qbzf_em")
async def get_stock_qbzf_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_qbzf_em/overview")
async def get_stock_qbzf_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取增发数据概览"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_qbzf_em/refresh")
async def refresh_stock_qbzf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_qbzf_em/clear")
async def clear_stock_qbzf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.clear_data()
