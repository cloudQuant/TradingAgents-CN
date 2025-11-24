
# 赚钱效应分析 - stock_market_activity_legu
@router.get("/collections/stock_market_activity_legu")
async def get_stock_market_activity_legu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取赚钱效应分析数据"""
    from app.services.stock.stock_market_activity_legu_service import StockMarketActivityLeguService
    service = StockMarketActivityLeguService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_market_activity_legu/overview")
async def get_stock_market_activity_legu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取赚钱效应分析数据概览"""
    from app.services.stock.stock_market_activity_legu_service import StockMarketActivityLeguService
    service = StockMarketActivityLeguService(db)
    return await service.get_overview()


@router.post("/collections/stock_market_activity_legu/refresh")
async def refresh_stock_market_activity_legu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新赚钱效应分析数据"""
    from app.services.stock.stock_market_activity_legu_service import StockMarketActivityLeguService
    service = StockMarketActivityLeguService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_market_activity_legu/clear")
async def clear_stock_market_activity_legu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空赚钱效应分析数据"""
    from app.services.stock.stock_market_activity_legu_service import StockMarketActivityLeguService
    service = StockMarketActivityLeguService(db)
    return await service.clear_data()
