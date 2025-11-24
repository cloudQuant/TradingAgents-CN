
# 富途牛牛-美股概念-成分股 - stock_concept_cons_futu
@router.get("/collections/stock_concept_cons_futu")
async def get_stock_concept_cons_futu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_concept_cons_futu/overview")
async def get_stock_concept_cons_futu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取富途牛牛-美股概念-成分股数据概览"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.get_overview()


@router.post("/collections/stock_concept_cons_futu/refresh")
async def refresh_stock_concept_cons_futu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_concept_cons_futu/clear")
async def clear_stock_concept_cons_futu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.clear_data()
