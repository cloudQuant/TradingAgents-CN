
# 龙虎榜-营业部排行-资金实力最强 - stock_lh_yyb_capital
@router.get("/collections/stock_lh_yyb_capital")
async def get_stock_lh_yyb_capital(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_capital/overview")
async def get_stock_lh_yyb_capital_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-资金实力最强数据概览"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_capital/refresh")
async def refresh_stock_lh_yyb_capital(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_capital/clear")
async def clear_stock_lh_yyb_capital(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.clear_data()
