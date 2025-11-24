
# 东方财富-成份股 - stock_board_concept_cons_em
@router.get("/collections/stock_board_concept_cons_em")
async def get_stock_board_concept_cons_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_cons_em/overview")
async def get_stock_board_concept_cons_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据概览"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_cons_em/refresh")
async def refresh_stock_board_concept_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_cons_em/clear")
async def clear_stock_board_concept_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.clear_data()
