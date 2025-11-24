
# 个股信息查询-东财 - stock_individual_info_em
@router.get("/collections/stock_individual_info_em")
async def get_stock_individual_info_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_info_em/overview")
async def get_stock_individual_info_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-东财数据概览"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_info_em/refresh")
async def refresh_stock_individual_info_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_info_em/clear")
async def clear_stock_individual_info_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.clear_data()
