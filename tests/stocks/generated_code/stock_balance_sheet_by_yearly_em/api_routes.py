
# 资产负债表-按年度 - stock_balance_sheet_by_yearly_em
@router.get("/collections/stock_balance_sheet_by_yearly_em")
async def get_stock_balance_sheet_by_yearly_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-按年度数据"""
    from app.services.stock.stock_balance_sheet_by_yearly_em_service import StockBalanceSheetByYearlyEmService
    service = StockBalanceSheetByYearlyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_balance_sheet_by_yearly_em/overview")
async def get_stock_balance_sheet_by_yearly_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-按年度数据概览"""
    from app.services.stock.stock_balance_sheet_by_yearly_em_service import StockBalanceSheetByYearlyEmService
    service = StockBalanceSheetByYearlyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_balance_sheet_by_yearly_em/refresh")
async def refresh_stock_balance_sheet_by_yearly_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新资产负债表-按年度数据"""
    from app.services.stock.stock_balance_sheet_by_yearly_em_service import StockBalanceSheetByYearlyEmService
    service = StockBalanceSheetByYearlyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_balance_sheet_by_yearly_em/clear")
async def clear_stock_balance_sheet_by_yearly_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空资产负债表-按年度数据"""
    from app.services.stock.stock_balance_sheet_by_yearly_em_service import StockBalanceSheetByYearlyEmService
    service = StockBalanceSheetByYearlyEmService(db)
    return await service.clear_data()
