
# 同花顺-指数 - stock_board_industry_index_ths
@router.get("/collections/stock_board_industry_index_ths")
async def get_stock_board_industry_index_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_index_ths/overview")
async def get_stock_board_industry_index_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-指数数据概览"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_index_ths/refresh")
async def refresh_stock_board_industry_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_index_ths/clear")
async def clear_stock_board_industry_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.clear_data()
