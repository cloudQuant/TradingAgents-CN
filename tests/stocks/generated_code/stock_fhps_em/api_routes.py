
# 分红配送-东财 - stock_fhps_em
@router.get("/collections/stock_fhps_em")
async def get_stock_fhps_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_fhps_em/overview")
async def get_stock_fhps_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送-东财数据概览"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_fhps_em/refresh")
async def refresh_stock_fhps_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_fhps_em/clear")
async def clear_stock_fhps_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.clear_data()
