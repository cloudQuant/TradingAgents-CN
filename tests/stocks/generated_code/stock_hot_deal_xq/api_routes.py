
# 交易排行榜 - stock_hot_deal_xq
@router.get("/collections/stock_hot_deal_xq")
async def get_stock_hot_deal_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_deal_xq/overview")
async def get_stock_hot_deal_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取交易排行榜数据概览"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_deal_xq/refresh")
async def refresh_stock_hot_deal_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_deal_xq/clear")
async def clear_stock_hot_deal_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.clear_data()
