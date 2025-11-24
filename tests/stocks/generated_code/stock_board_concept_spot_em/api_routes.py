
# 东方财富-概念板块-实时行情 - stock_board_concept_spot_em
@router.get("/collections/stock_board_concept_spot_em")
async def get_stock_board_concept_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_spot_em/overview")
async def get_stock_board_concept_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块-实时行情数据概览"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_spot_em/refresh")
async def refresh_stock_board_concept_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_spot_em/clear")
async def clear_stock_board_concept_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.clear_data()
