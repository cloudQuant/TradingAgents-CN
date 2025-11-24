
# 历史评分 - stock_comment_detail_zhpj_lspf_em
@router.get("/collections/stock_comment_detail_zhpj_lspf_em")
async def get_stock_comment_detail_zhpj_lspf_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史评分数据"""
    from app.services.stock.stock_comment_detail_zhpj_lspf_em_service import StockCommentDetailZhpjLspfEmService
    service = StockCommentDetailZhpjLspfEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_comment_detail_zhpj_lspf_em/overview")
async def get_stock_comment_detail_zhpj_lspf_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史评分数据概览"""
    from app.services.stock.stock_comment_detail_zhpj_lspf_em_service import StockCommentDetailZhpjLspfEmService
    service = StockCommentDetailZhpjLspfEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_comment_detail_zhpj_lspf_em/refresh")
async def refresh_stock_comment_detail_zhpj_lspf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史评分数据"""
    from app.services.stock.stock_comment_detail_zhpj_lspf_em_service import StockCommentDetailZhpjLspfEmService
    service = StockCommentDetailZhpjLspfEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_comment_detail_zhpj_lspf_em/clear")
async def clear_stock_comment_detail_zhpj_lspf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史评分数据"""
    from app.services.stock.stock_comment_detail_zhpj_lspf_em_service import StockCommentDetailZhpjLspfEmService
    service = StockCommentDetailZhpjLspfEmService(db)
    return await service.clear_data()
