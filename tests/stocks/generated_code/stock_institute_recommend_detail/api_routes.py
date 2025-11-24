
# 股票评级记录 - stock_institute_recommend_detail
@router.get("/collections/stock_institute_recommend_detail")
async def get_stock_institute_recommend_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_recommend_detail/overview")
async def get_stock_institute_recommend_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票评级记录数据概览"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_recommend_detail/refresh")
async def refresh_stock_institute_recommend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_recommend_detail/clear")
async def clear_stock_institute_recommend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.clear_data()
