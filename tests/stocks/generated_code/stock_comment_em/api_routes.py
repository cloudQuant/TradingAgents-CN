
# 千股千评 - stock_comment_em
@router.get("/collections/stock_comment_em")
async def get_stock_comment_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取千股千评数据"""
    from app.services.stock.stock_comment_em_service import StockCommentEmService
    service = StockCommentEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_em/overview")
async def get_stock_comment_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取千股千评数据概览"""
    from app.services.stock.stock_comment_em_service import StockCommentEmService
    service = StockCommentEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_em/refresh")
async def refresh_stock_comment_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新千股千评数据"""
    from app.services.stock.stock_comment_em_service import StockCommentEmService
    service = StockCommentEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_em/clear")
async def clear_stock_comment_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空千股千评数据"""
    from app.services.stock.stock_comment_em_service import StockCommentEmService
    service = StockCommentEmService(db)
    return await service.clear_data()
