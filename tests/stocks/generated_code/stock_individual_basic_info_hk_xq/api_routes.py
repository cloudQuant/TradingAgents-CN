
# 个股信息查询-雪球 - stock_individual_basic_info_hk_xq
@router.get("/collections/stock_individual_basic_info_hk_xq")
async def get_stock_individual_basic_info_hk_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_basic_info_hk_xq/overview")
async def get_stock_individual_basic_info_hk_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据概览"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_basic_info_hk_xq/refresh")
async def refresh_stock_individual_basic_info_hk_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_basic_info_hk_xq/clear")
async def clear_stock_individual_basic_info_hk_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.clear_data()
