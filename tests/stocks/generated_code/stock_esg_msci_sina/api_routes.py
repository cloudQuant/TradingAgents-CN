
# MSCI - stock_esg_msci_sina
@router.get("/collections/stock_esg_msci_sina")
async def get_stock_esg_msci_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_msci_sina/overview")
async def get_stock_esg_msci_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取MSCI数据概览"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_msci_sina/refresh")
async def refresh_stock_esg_msci_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_msci_sina/clear")
async def clear_stock_esg_msci_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.clear_data()
