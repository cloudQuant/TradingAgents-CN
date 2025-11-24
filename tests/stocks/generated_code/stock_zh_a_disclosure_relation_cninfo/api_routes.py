
# 信息披露调研-巨潮资讯 - stock_zh_a_disclosure_relation_cninfo
@router.get("/collections/stock_zh_a_disclosure_relation_cninfo")
async def get_stock_zh_a_disclosure_relation_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_disclosure_relation_cninfo/overview")
async def get_stock_zh_a_disclosure_relation_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露调研-巨潮资讯数据概览"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_disclosure_relation_cninfo/refresh")
async def refresh_stock_zh_a_disclosure_relation_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_disclosure_relation_cninfo/clear")
async def clear_stock_zh_a_disclosure_relation_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.clear_data()
