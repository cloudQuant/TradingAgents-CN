
# 沪 A 股 - stock_sh_a_spot_em
@router.get("/collections/stock_sh_a_spot_em")
async def get_stock_sh_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sh_a_spot_em/overview")
async def get_stock_sh_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪 A 股数据概览"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sh_a_spot_em/refresh")
async def refresh_stock_sh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sh_a_spot_em/clear")
async def clear_stock_sh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.clear_data()
