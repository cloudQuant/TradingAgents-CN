
# IPO 受益股 - stock_ipo_benefit_ths
@router.get("/collections/stock_ipo_benefit_ths")
async def get_stock_ipo_benefit_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_benefit_ths/overview")
async def get_stock_ipo_benefit_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取IPO 受益股数据概览"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_benefit_ths/refresh")
async def refresh_stock_ipo_benefit_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_benefit_ths/clear")
async def clear_stock_ipo_benefit_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.clear_data()
