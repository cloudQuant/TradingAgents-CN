
# 龙虎榜-营业上榜统计 - stock_lhb_yytj_sina
@router.get("/collections/stock_lhb_yytj_sina")
async def get_stock_lhb_yytj_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_yytj_sina/overview")
async def get_stock_lhb_yytj_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业上榜统计数据概览"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_yytj_sina/refresh")
async def refresh_stock_lhb_yytj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_yytj_sina/clear")
async def clear_stock_lhb_yytj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.clear_data()
