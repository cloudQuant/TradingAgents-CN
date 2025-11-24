
# 两融账户信息 - stock_margin_account_info
@router.get("/collections/stock_margin_account_info")
async def get_stock_margin_account_info(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_account_info/overview")
async def get_stock_margin_account_info_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两融账户信息数据概览"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_account_info/refresh")
async def refresh_stock_margin_account_info(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_account_info/clear")
async def clear_stock_margin_account_info(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.clear_data()
