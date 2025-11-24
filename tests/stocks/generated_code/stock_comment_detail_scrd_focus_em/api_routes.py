
# 用户关注指数 - stock_comment_detail_scrd_focus_em
@router.get("/collections/stock_comment_detail_scrd_focus_em")
async def get_stock_comment_detail_scrd_focus_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取用户关注指数数据"""
    from app.services.stock.stock_comment_detail_scrd_focus_em_service import StockCommentDetailScrdFocusEmService
    service = StockCommentDetailScrdFocusEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_detail_scrd_focus_em/overview")
async def get_stock_comment_detail_scrd_focus_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取用户关注指数数据概览"""
    from app.services.stock.stock_comment_detail_scrd_focus_em_service import StockCommentDetailScrdFocusEmService
    service = StockCommentDetailScrdFocusEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_detail_scrd_focus_em/refresh")
async def refresh_stock_comment_detail_scrd_focus_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新用户关注指数数据"""
    from app.services.stock.stock_comment_detail_scrd_focus_em_service import StockCommentDetailScrdFocusEmService
    service = StockCommentDetailScrdFocusEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_detail_scrd_focus_em/clear")
async def clear_stock_comment_detail_scrd_focus_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空用户关注指数数据"""
    from app.services.stock.stock_comment_detail_scrd_focus_em_service import StockCommentDetailScrdFocusEmService
    service = StockCommentDetailScrdFocusEmService(db)
    return await service.clear_data()
