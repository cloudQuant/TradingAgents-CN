
# 龙虎榜-营业部排行-抱团操作实力 - stock_lh_yyb_control
@router.get("/collections/stock_lh_yyb_control")
async def get_stock_lh_yyb_control(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_control/overview")
async def get_stock_lh_yyb_control_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-抱团操作实力数据概览"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_control/refresh")
async def refresh_stock_lh_yyb_control(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_control/clear")
async def clear_stock_lh_yyb_control(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.clear_data()
