
# 市场参与意愿 - stock_comment_detail_scrd_desire_em
@router.get("/collections/stock_comment_detail_scrd_desire_em")
async def get_stock_comment_detail_scrd_desire_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_em_service import StockCommentDetailScrdDesireEmService
    service = StockCommentDetailScrdDesireEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_detail_scrd_desire_em/overview")
async def get_stock_comment_detail_scrd_desire_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取市场参与意愿数据概览"""
    from app.services.stock.stock_comment_detail_scrd_desire_em_service import StockCommentDetailScrdDesireEmService
    service = StockCommentDetailScrdDesireEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_detail_scrd_desire_em/refresh")
async def refresh_stock_comment_detail_scrd_desire_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_em_service import StockCommentDetailScrdDesireEmService
    service = StockCommentDetailScrdDesireEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_detail_scrd_desire_em/clear")
async def clear_stock_comment_detail_scrd_desire_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空市场参与意愿数据"""
    from app.services.stock.stock_comment_detail_scrd_desire_em_service import StockCommentDetailScrdDesireEmService
    service = StockCommentDetailScrdDesireEmService(db)
    return await service.clear_data()
