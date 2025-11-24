
# 日度市场参与意愿 - stock_comment_detail_scrd_desire_daily_em
@router.get("/collections/stock_comment_detail_scrd_desire_daily_em")
async def get_stock_comment_detail_scrd_desire_daily_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日度市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_daily_em_service import StockCommentDetailScrdDesireDailyEmService
    service = StockCommentDetailScrdDesireDailyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_detail_scrd_desire_daily_em/overview")
async def get_stock_comment_detail_scrd_desire_daily_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日度市场参与意愿数据概览"""
    from app.services.stock.stock_comment_detail_scrd_desire_daily_em_service import StockCommentDetailScrdDesireDailyEmService
    service = StockCommentDetailScrdDesireDailyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_detail_scrd_desire_daily_em/refresh")
async def refresh_stock_comment_detail_scrd_desire_daily_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新日度市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_daily_em_service import StockCommentDetailScrdDesireDailyEmService
    service = StockCommentDetailScrdDesireDailyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_detail_scrd_desire_daily_em/clear")
async def clear_stock_comment_detail_scrd_desire_daily_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空日度市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_daily_em_service import StockCommentDetailScrdDesireDailyEmService
    service = StockCommentDetailScrdDesireDailyEmService(db)
    return await service.clear_data()
