
# 路孚特 - stock_esg_rft_sina
@router.get("/collections/stock_esg_rft_sina")
async def get_stock_esg_rft_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_rft_sina/overview")
async def get_stock_esg_rft_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取路孚特数据概览"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_rft_sina/refresh")
async def refresh_stock_esg_rft_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_rft_sina/clear")
async def clear_stock_esg_rft_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.clear_data()
