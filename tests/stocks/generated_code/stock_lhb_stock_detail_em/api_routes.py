
# 个股龙虎榜详情 - stock_lhb_stock_detail_em
@router.get("/collections/stock_lhb_stock_detail_em")
async def get_stock_lhb_stock_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_stock_detail_em/overview")
async def get_stock_lhb_stock_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股龙虎榜详情数据概览"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_stock_detail_em/refresh")
async def refresh_stock_lhb_stock_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_stock_detail_em/clear")
async def clear_stock_lhb_stock_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.clear_data()
