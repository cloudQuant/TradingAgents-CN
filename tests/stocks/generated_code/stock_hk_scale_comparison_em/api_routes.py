
# 规模对比 - stock_hk_scale_comparison_em
@router.get("/collections/stock_hk_scale_comparison_em")
async def get_stock_hk_scale_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取规模对比数据"""
    from app.services.stock.stock_hk_scale_comparison_em_service import StockHkScaleComparisonEmService
    service = StockHkScaleComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_scale_comparison_em/overview")
async def get_stock_hk_scale_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取规模对比数据概览"""
    from app.services.stock.stock_hk_scale_comparison_em_service import StockHkScaleComparisonEmService
    service = StockHkScaleComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_scale_comparison_em/refresh")
async def refresh_stock_hk_scale_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新规模对比数据"""
    from app.services.stock.stock_hk_scale_comparison_em_service import StockHkScaleComparisonEmService
    service = StockHkScaleComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_scale_comparison_em/clear")
async def clear_stock_hk_scale_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空规模对比数据"""
    from app.services.stock.stock_hk_scale_comparison_em_service import StockHkScaleComparisonEmService
    service = StockHkScaleComparisonEmService(db)
    return await service.clear_data()
