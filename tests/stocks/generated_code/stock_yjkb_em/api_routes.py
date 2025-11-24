
# 业绩快报 - stock_yjkb_em
@router.get("/collections/stock_yjkb_em")
async def get_stock_yjkb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_yjkb_em/overview")
async def get_stock_yjkb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩快报数据概览"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_yjkb_em/refresh")
async def refresh_stock_yjkb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_yjkb_em/clear")
async def clear_stock_yjkb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.clear_data()
