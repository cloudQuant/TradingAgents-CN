
# 公司动态 - stock_gsrl_gsdt_em
@router.get("/collections/stock_gsrl_gsdt_em")
async def get_stock_gsrl_gsdt_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gsrl_gsdt_em/overview")
async def get_stock_gsrl_gsdt_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司动态数据概览"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gsrl_gsdt_em/refresh")
async def refresh_stock_gsrl_gsdt_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gsrl_gsdt_em/clear")
async def clear_stock_gsrl_gsdt_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.clear_data()
