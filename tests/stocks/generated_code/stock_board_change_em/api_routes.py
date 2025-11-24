
# 板块异动详情 - stock_board_change_em
@router.get("/collections/stock_board_change_em")
async def get_stock_board_change_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_change_em/overview")
async def get_stock_board_change_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块异动详情数据概览"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_change_em/refresh")
async def refresh_stock_board_change_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_change_em/clear")
async def clear_stock_board_change_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.clear_data()
