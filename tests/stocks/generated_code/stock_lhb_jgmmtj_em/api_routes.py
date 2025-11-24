
# 机构买卖每日统计 - stock_lhb_jgmmtj_em
@router.get("/collections/stock_lhb_jgmmtj_em")
async def get_stock_lhb_jgmmtj_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgmmtj_em/overview")
async def get_stock_lhb_jgmmtj_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构买卖每日统计数据概览"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgmmtj_em/refresh")
async def refresh_stock_lhb_jgmmtj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgmmtj_em/clear")
async def clear_stock_lhb_jgmmtj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.clear_data()
