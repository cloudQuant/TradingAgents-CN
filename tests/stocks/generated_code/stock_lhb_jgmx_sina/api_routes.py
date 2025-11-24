
# 龙虎榜-机构席位成交明细 - stock_lhb_jgmx_sina
@router.get("/collections/stock_lhb_jgmx_sina")
async def get_stock_lhb_jgmx_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgmx_sina/overview")
async def get_stock_lhb_jgmx_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位成交明细数据概览"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgmx_sina/refresh")
async def refresh_stock_lhb_jgmx_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgmx_sina/clear")
async def clear_stock_lhb_jgmx_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.clear_data()
