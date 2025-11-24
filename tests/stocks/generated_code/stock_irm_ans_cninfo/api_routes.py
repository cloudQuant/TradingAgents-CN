
# 互动易-回答 - stock_irm_ans_cninfo
@router.get("/collections/stock_irm_ans_cninfo")
async def get_stock_irm_ans_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_irm_ans_cninfo/overview")
async def get_stock_irm_ans_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-回答数据概览"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_irm_ans_cninfo/refresh")
async def refresh_stock_irm_ans_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_irm_ans_cninfo/clear")
async def clear_stock_irm_ans_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.clear_data()
