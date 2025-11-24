
# 股东持股明细-十大股东 - stock_gdfx_holding_detail_em
@router.get("/collections/stock_gdfx_holding_detail_em")
async def get_stock_gdfx_holding_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_holding_detail_em/overview")
async def get_stock_gdfx_holding_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大股东数据概览"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_holding_detail_em/refresh")
async def refresh_stock_gdfx_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_holding_detail_em/clear")
async def clear_stock_gdfx_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.clear_data()
