
# 股票列表-A股 - stock_info_a_code_name
@router.get("/collections/stock_info_a_code_name")
async def get_stock_info_a_code_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_a_code_name/overview")
async def get_stock_info_a_code_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-A股数据概览"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_a_code_name/refresh")
async def refresh_stock_info_a_code_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_a_code_name/clear")
async def clear_stock_info_a_code_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.clear_data()
