
# 营业部排行 - stock_dzjy_yybph
@router.get("/collections/stock_dzjy_yybph")
async def get_stock_dzjy_yybph(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_yybph/overview")
async def get_stock_dzjy_yybph_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据概览"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_yybph/refresh")
async def refresh_stock_dzjy_yybph(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_yybph/clear")
async def clear_stock_dzjy_yybph(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.clear_data()
