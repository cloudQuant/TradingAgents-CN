
# 华证指数 - stock_esg_hz_sina
@router.get("/collections/stock_esg_hz_sina")
async def get_stock_esg_hz_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_hz_sina/overview")
async def get_stock_esg_hz_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取华证指数数据概览"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_hz_sina/refresh")
async def refresh_stock_esg_hz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_hz_sina/clear")
async def clear_stock_esg_hz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.clear_data()
