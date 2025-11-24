
# 融资融券明细 - stock_margin_detail_sse
@router.get("/collections/stock_margin_detail_sse")
async def get_stock_margin_detail_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_detail_sse/overview")
async def get_stock_margin_detail_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据概览"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_detail_sse/refresh")
async def refresh_stock_margin_detail_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_detail_sse/clear")
async def clear_stock_margin_detail_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.clear_data()
