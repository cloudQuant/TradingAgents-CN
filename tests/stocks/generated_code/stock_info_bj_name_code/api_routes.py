
# 股票列表-北证 - stock_info_bj_name_code
@router.get("/collections/stock_info_bj_name_code")
async def get_stock_info_bj_name_code(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_bj_name_code/overview")
async def get_stock_info_bj_name_code_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-北证数据概览"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_bj_name_code/refresh")
async def refresh_stock_info_bj_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_bj_name_code/clear")
async def clear_stock_info_bj_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.clear_data()
