
# 机构参与度 - stock_comment_detail_zlkp_jgcyd_em
@router.get("/collections/stock_comment_detail_zlkp_jgcyd_em")
async def get_stock_comment_detail_zlkp_jgcyd_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构参与度数据"""
    from app.services.stock.stock_comment_detail_zlkp_jgcyd_em_service import StockCommentDetailZlkpJgcydEmService
    service = StockCommentDetailZlkpJgcydEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_detail_zlkp_jgcyd_em/overview")
async def get_stock_comment_detail_zlkp_jgcyd_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构参与度数据概览"""
    from app.services.stock.stock_comment_detail_zlkp_jgcyd_em_service import StockCommentDetailZlkpJgcydEmService
    service = StockCommentDetailZlkpJgcydEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_detail_zlkp_jgcyd_em/refresh")
async def refresh_stock_comment_detail_zlkp_jgcyd_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构参与度数据"""
    from app.services.stock.stock_comment_detail_zlkp_jgcyd_em_service import StockCommentDetailZlkpJgcydEmService
    service = StockCommentDetailZlkpJgcydEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_detail_zlkp_jgcyd_em/clear")
async def clear_stock_comment_detail_zlkp_jgcyd_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构参与度数据"""
    from app.services.stock.stock_comment_detail_zlkp_jgcyd_em_service import StockCommentDetailZlkpJgcydEmService
    service = StockCommentDetailZlkpJgcydEmService(db)
    return await service.clear_data()
