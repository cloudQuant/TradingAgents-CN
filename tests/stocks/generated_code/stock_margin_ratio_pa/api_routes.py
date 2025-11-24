
# 标的证券名单及保证金比例查询 - stock_margin_ratio_pa
@router.get("/collections/stock_margin_ratio_pa")
async def get_stock_margin_ratio_pa(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_ratio_pa/overview")
async def get_stock_margin_ratio_pa_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券名单及保证金比例查询数据概览"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_ratio_pa/refresh")
async def refresh_stock_margin_ratio_pa(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_ratio_pa/clear")
async def clear_stock_margin_ratio_pa(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.clear_data()
