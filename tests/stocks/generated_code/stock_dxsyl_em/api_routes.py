
# 打新收益率 - stock_dxsyl_em
@router.get("/collections/stock_dxsyl_em")
async def get_stock_dxsyl_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取打新收益率数据"""
    from app.services.stock.stock_dxsyl_em_service import StockDxsylEmService
    service = StockDxsylEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dxsyl_em/overview")
async def get_stock_dxsyl_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取打新收益率数据概览"""
    from app.services.stock.stock_dxsyl_em_service import StockDxsylEmService
    service = StockDxsylEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_dxsyl_em/refresh")
async def refresh_stock_dxsyl_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新打新收益率数据"""
    from app.services.stock.stock_dxsyl_em_service import StockDxsylEmService
    service = StockDxsylEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dxsyl_em/clear")
async def clear_stock_dxsyl_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空打新收益率数据"""
    from app.services.stock.stock_dxsyl_em_service import StockDxsylEmService
    service = StockDxsylEmService(db)
    return await service.clear_data()
