
# 龙虎榜-营业部排行-上榜次数最多 - stock_lh_yyb_most
@router.get("/collections/stock_lh_yyb_most")
async def get_stock_lh_yyb_most(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_most/overview")
async def get_stock_lh_yyb_most_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-上榜次数最多数据概览"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_most/refresh")
async def refresh_stock_lh_yyb_most(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_most/clear")
async def clear_stock_lh_yyb_most(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.clear_data()
