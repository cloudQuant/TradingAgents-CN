
# 机构推荐池 - stock_institute_recommend
@router.get("/collections/stock_institute_recommend")
async def get_stock_institute_recommend(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_recommend/overview")
async def get_stock_institute_recommend_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构推荐池数据概览"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_recommend/refresh")
async def refresh_stock_institute_recommend(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_recommend/clear")
async def clear_stock_institute_recommend(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.clear_data()
