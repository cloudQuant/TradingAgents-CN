
# 秩鼎 - stock_esg_zd_sina
@router.get("/collections/stock_esg_zd_sina")
async def get_stock_esg_zd_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_zd_sina/overview")
async def get_stock_esg_zd_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取秩鼎数据概览"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_zd_sina/refresh")
async def refresh_stock_esg_zd_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_zd_sina/clear")
async def clear_stock_esg_zd_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.clear_data()
