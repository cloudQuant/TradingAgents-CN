
# 券商业绩月报 - stock_qsjy_em
@router.get("/collections/stock_qsjy_em")
async def get_stock_qsjy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_qsjy_em/overview")
async def get_stock_qsjy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取券商业绩月报数据概览"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_qsjy_em/refresh")
async def refresh_stock_qsjy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_qsjy_em/clear")
async def clear_stock_qsjy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.clear_data()
