
# 股债利差 - stock_ebs_lg
@router.get("/collections/stock_ebs_lg")
async def get_stock_ebs_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ebs_lg/overview")
async def get_stock_ebs_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股债利差数据概览"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_ebs_lg/refresh")
async def refresh_stock_ebs_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ebs_lg/clear")
async def clear_stock_ebs_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.clear_data()
