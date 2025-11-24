"""
生成的API路由代码
需要手动添加到 app/routers/stocks.py 文件中
"""

# 将以下代码添加到 app/routers/stocks.py 的路由定义中
# 注意: 需要先导入必要的依赖


# 财报发行 - news_report_time_baidu
@router.get("/collections/news_report_time_baidu")
async def get_news_report_time_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_report_time_baidu/overview")
async def get_news_report_time_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财报发行数据概览"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_report_time_baidu/refresh")
async def refresh_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_report_time_baidu/clear")
async def clear_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.clear_data()



# 分红派息 - news_trade_notify_dividend_baidu
@router.get("/collections/news_trade_notify_dividend_baidu")
async def get_news_trade_notify_dividend_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_trade_notify_dividend_baidu/overview")
async def get_news_trade_notify_dividend_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据概览"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_trade_notify_dividend_baidu/refresh")
async def refresh_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_trade_notify_dividend_baidu/clear")
async def clear_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.clear_data()



# 停复牌 - news_trade_notify_suspend_baidu
@router.get("/collections/news_trade_notify_suspend_baidu")
async def get_news_trade_notify_suspend_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取停复牌数据"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_trade_notify_suspend_baidu/overview")
async def get_news_trade_notify_suspend_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取停复牌数据概览"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_trade_notify_suspend_baidu/refresh")
async def refresh_news_trade_notify_suspend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新停复牌数据"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_trade_notify_suspend_baidu/clear")
async def clear_news_trade_notify_suspend_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空停复牌数据"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.clear_data()



# A 股等权重与中位数市净率 - stock_a_all_pb
@router.get("/collections/stock_a_all_pb")
async def get_stock_a_all_pb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_all_pb/overview")
async def get_stock_a_all_pb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市净率数据概览"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_all_pb/refresh")
async def refresh_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_all_pb/clear")
async def clear_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.clear_data()



# 破净股统计 - stock_a_below_net_asset_statistics
@router.get("/collections/stock_a_below_net_asset_statistics")
async def get_stock_a_below_net_asset_statistics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_below_net_asset_statistics/overview")
async def get_stock_a_below_net_asset_statistics_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取破净股统计数据概览"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_below_net_asset_statistics/refresh")
async def refresh_stock_a_below_net_asset_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_below_net_asset_statistics/clear")
async def clear_stock_a_below_net_asset_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空破净股统计数据"""
    from app.services.stock.stock_a_below_net_asset_statistics_service import StockABelowNetAssetStatisticsService
    service = StockABelowNetAssetStatisticsService(db)
    return await service.clear_data()



# 大盘拥挤度 - stock_a_congestion_lg
@router.get("/collections/stock_a_congestion_lg")
async def get_stock_a_congestion_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_congestion_lg/overview")
async def get_stock_a_congestion_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取大盘拥挤度数据概览"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_congestion_lg/refresh")
async def refresh_stock_a_congestion_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_congestion_lg/clear")
async def clear_stock_a_congestion_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空大盘拥挤度数据"""
    from app.services.stock.stock_a_congestion_lg_service import StockACongestionLgService
    service = StockACongestionLgService(db)
    return await service.clear_data()



# A 股股息率 - stock_a_gxl_lg
@router.get("/collections/stock_a_gxl_lg")
async def get_stock_a_gxl_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股股息率数据"""
    from app.services.stock.stock_a_gxl_lg_service import StockAGxlLgService
    service = StockAGxlLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_gxl_lg/overview")
async def get_stock_a_gxl_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股股息率数据概览"""
    from app.services.stock.stock_a_gxl_lg_service import StockAGxlLgService
    service = StockAGxlLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_gxl_lg/refresh")
async def refresh_stock_a_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股股息率数据"""
    from app.services.stock.stock_a_gxl_lg_service import StockAGxlLgService
    service = StockAGxlLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_gxl_lg/clear")
async def clear_stock_a_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股股息率数据"""
    from app.services.stock.stock_a_gxl_lg_service import StockAGxlLgService
    service = StockAGxlLgService(db)
    return await service.clear_data()



# 创新高和新低的股票数量 - stock_a_high_low_statistics
@router.get("/collections/stock_a_high_low_statistics")
async def get_stock_a_high_low_statistics(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_high_low_statistics/overview")
async def get_stock_a_high_low_statistics_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创新高和新低的股票数量数据概览"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_high_low_statistics/refresh")
async def refresh_stock_a_high_low_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_high_low_statistics/clear")
async def clear_stock_a_high_low_statistics(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空创新高和新低的股票数量数据"""
    from app.services.stock.stock_a_high_low_statistics_service import StockAHighLowStatisticsService
    service = StockAHighLowStatisticsService(db)
    return await service.clear_data()



# A 股等权重与中位数市盈率 - stock_a_ttm_lyr
@router.get("/collections/stock_a_ttm_lyr")
async def get_stock_a_ttm_lyr(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_ttm_lyr/overview")
async def get_stock_a_ttm_lyr_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股等权重与中位数市盈率数据概览"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_ttm_lyr/refresh")
async def refresh_stock_a_ttm_lyr(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_ttm_lyr/clear")
async def clear_stock_a_ttm_lyr(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股等权重与中位数市盈率数据"""
    from app.services.stock.stock_a_ttm_lyr_service import StockATtmLyrService
    service = StockATtmLyrService(db)
    return await service.clear_data()



# 股票账户统计月度 - stock_account_statistics_em
@router.get("/collections/stock_account_statistics_em")
async def get_stock_account_statistics_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_account_statistics_em/overview")
async def get_stock_account_statistics_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票账户统计月度数据概览"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_account_statistics_em/refresh")
async def refresh_stock_account_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_account_statistics_em/clear")
async def clear_stock_account_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票账户统计月度数据"""
    from app.services.stock.stock_account_statistics_em_service import StockAccountStatisticsEmService
    service = StockAccountStatisticsEmService(db)
    return await service.clear_data()



# 股票增发 - stock_add_stock
@router.get("/collections/stock_add_stock")
async def get_stock_add_stock(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_add_stock/overview")
async def get_stock_add_stock_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票增发数据概览"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.get_overview()


@router.post("/collections/stock_add_stock/refresh")
async def refresh_stock_add_stock(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_add_stock/clear")
async def clear_stock_add_stock(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票增发数据"""
    from app.services.stock.stock_add_stock_service import StockAddStockService
    service = StockAddStockService(db)
    return await service.clear_data()



# 配股实施方案-巨潮资讯 - stock_allotment_cninfo
@router.get("/collections/stock_allotment_cninfo")
async def get_stock_allotment_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_allotment_cninfo/overview")
async def get_stock_allotment_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股实施方案-巨潮资讯数据概览"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_allotment_cninfo/refresh")
async def refresh_stock_allotment_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_allotment_cninfo/clear")
async def clear_stock_allotment_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空配股实施方案-巨潮资讯数据"""
    from app.services.stock.stock_allotment_cninfo_service import StockAllotmentCninfoService
    service = StockAllotmentCninfoService(db)
    return await service.clear_data()



# 分析师详情 - stock_analyst_detail_em
@router.get("/collections/stock_analyst_detail_em")
async def get_stock_analyst_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分析师详情数据"""
    from app.services.stock.stock_analyst_detail_em_service import StockAnalystDetailEmService
    service = StockAnalystDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_analyst_detail_em/overview")
async def get_stock_analyst_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分析师详情数据概览"""
    from app.services.stock.stock_analyst_detail_em_service import StockAnalystDetailEmService
    service = StockAnalystDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_analyst_detail_em/refresh")
async def refresh_stock_analyst_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分析师详情数据"""
    from app.services.stock.stock_analyst_detail_em_service import StockAnalystDetailEmService
    service = StockAnalystDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_analyst_detail_em/clear")
async def clear_stock_analyst_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分析师详情数据"""
    from app.services.stock.stock_analyst_detail_em_service import StockAnalystDetailEmService
    service = StockAnalystDetailEmService(db)
    return await service.clear_data()



# 分析师指数排行 - stock_analyst_rank_em
@router.get("/collections/stock_analyst_rank_em")
async def get_stock_analyst_rank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分析师指数排行数据"""
    from app.services.stock.stock_analyst_rank_em_service import StockAnalystRankEmService
    service = StockAnalystRankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_analyst_rank_em/overview")
async def get_stock_analyst_rank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分析师指数排行数据概览"""
    from app.services.stock.stock_analyst_rank_em_service import StockAnalystRankEmService
    service = StockAnalystRankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_analyst_rank_em/refresh")
async def refresh_stock_analyst_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分析师指数排行数据"""
    from app.services.stock.stock_analyst_rank_em_service import StockAnalystRankEmService
    service = StockAnalystRankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_analyst_rank_em/clear")
async def clear_stock_analyst_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分析师指数排行数据"""
    from app.services.stock.stock_analyst_rank_em_service import StockAnalystRankEmService
    service = StockAnalystRankEmService(db)
    return await service.clear_data()



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



# 行情报价 - stock_bid_ask_em
@router.get("/collections/stock_bid_ask_em")
async def get_stock_bid_ask_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行情报价数据"""
    from app.services.stock.stock_bid_ask_em_service import StockBidAskEmService
    service = StockBidAskEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_bid_ask_em/overview")
async def get_stock_bid_ask_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行情报价数据概览"""
    from app.services.stock.stock_bid_ask_em_service import StockBidAskEmService
    service = StockBidAskEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_bid_ask_em/refresh")
async def refresh_stock_bid_ask_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行情报价数据"""
    from app.services.stock.stock_bid_ask_em_service import StockBidAskEmService
    service = StockBidAskEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_bid_ask_em/clear")
async def clear_stock_bid_ask_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行情报价数据"""
    from app.services.stock.stock_bid_ask_em_service import StockBidAskEmService
    service = StockBidAskEmService(db)
    return await service.clear_data()



# 京 A 股 - stock_bj_a_spot_em
@router.get("/collections/stock_bj_a_spot_em")
async def get_stock_bj_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_bj_a_spot_em/overview")
async def get_stock_bj_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取京 A 股数据概览"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_bj_a_spot_em/refresh")
async def refresh_stock_bj_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_bj_a_spot_em/clear")
async def clear_stock_bj_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空京 A 股数据"""
    from app.services.stock.stock_bj_a_spot_em_service import StockBjASpotEmService
    service = StockBjASpotEmService(db)
    return await service.clear_data()



# 板块异动详情 - stock_board_change_em
@router.get("/collections/stock_board_change_em")
async def get_stock_board_change_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_change_em/overview")
async def get_stock_board_change_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块异动详情数据概览"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_change_em/refresh")
async def refresh_stock_board_change_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_change_em/clear")
async def clear_stock_board_change_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块异动详情数据"""
    from app.services.stock.stock_board_change_em_service import StockBoardChangeEmService
    service = StockBoardChangeEmService(db)
    return await service.clear_data()



# 东方财富-成份股 - stock_board_concept_cons_em
@router.get("/collections/stock_board_concept_cons_em")
async def get_stock_board_concept_cons_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_cons_em/overview")
async def get_stock_board_concept_cons_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据概览"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_cons_em/refresh")
async def refresh_stock_board_concept_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_cons_em/clear")
async def clear_stock_board_concept_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-成份股数据"""
    from app.services.stock.stock_board_concept_cons_em_service import StockBoardConceptConsEmService
    service = StockBoardConceptConsEmService(db)
    return await service.clear_data()



# 东方财富-指数 - stock_board_concept_hist_em
@router.get("/collections/stock_board_concept_hist_em")
async def get_stock_board_concept_hist_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数数据"""
    from app.services.stock.stock_board_concept_hist_em_service import StockBoardConceptHistEmService
    service = StockBoardConceptHistEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_hist_em/overview")
async def get_stock_board_concept_hist_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数数据概览"""
    from app.services.stock.stock_board_concept_hist_em_service import StockBoardConceptHistEmService
    service = StockBoardConceptHistEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_hist_em/refresh")
async def refresh_stock_board_concept_hist_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-指数数据"""
    from app.services.stock.stock_board_concept_hist_em_service import StockBoardConceptHistEmService
    service = StockBoardConceptHistEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_hist_em/clear")
async def clear_stock_board_concept_hist_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-指数数据"""
    from app.services.stock.stock_board_concept_hist_em_service import StockBoardConceptHistEmService
    service = StockBoardConceptHistEmService(db)
    return await service.clear_data()



# 东方财富-指数-分时 - stock_board_concept_hist_min_em
@router.get("/collections/stock_board_concept_hist_min_em")
async def get_stock_board_concept_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-分时数据"""
    from app.services.stock.stock_board_concept_hist_min_em_service import StockBoardConceptHistMinEmService
    service = StockBoardConceptHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_hist_min_em/overview")
async def get_stock_board_concept_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-分时数据概览"""
    from app.services.stock.stock_board_concept_hist_min_em_service import StockBoardConceptHistMinEmService
    service = StockBoardConceptHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_hist_min_em/refresh")
async def refresh_stock_board_concept_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-指数-分时数据"""
    from app.services.stock.stock_board_concept_hist_min_em_service import StockBoardConceptHistMinEmService
    service = StockBoardConceptHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_hist_min_em/clear")
async def clear_stock_board_concept_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-指数-分时数据"""
    from app.services.stock.stock_board_concept_hist_min_em_service import StockBoardConceptHistMinEmService
    service = StockBoardConceptHistMinEmService(db)
    return await service.clear_data()



# 同花顺-概念板块指数 - stock_board_concept_index_ths
@router.get("/collections/stock_board_concept_index_ths")
async def get_stock_board_concept_index_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-概念板块指数数据"""
    from app.services.stock.stock_board_concept_index_ths_service import StockBoardConceptIndexThsService
    service = StockBoardConceptIndexThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_index_ths/overview")
async def get_stock_board_concept_index_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-概念板块指数数据概览"""
    from app.services.stock.stock_board_concept_index_ths_service import StockBoardConceptIndexThsService
    service = StockBoardConceptIndexThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_index_ths/refresh")
async def refresh_stock_board_concept_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新同花顺-概念板块指数数据"""
    from app.services.stock.stock_board_concept_index_ths_service import StockBoardConceptIndexThsService
    service = StockBoardConceptIndexThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_index_ths/clear")
async def clear_stock_board_concept_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空同花顺-概念板块指数数据"""
    from app.services.stock.stock_board_concept_index_ths_service import StockBoardConceptIndexThsService
    service = StockBoardConceptIndexThsService(db)
    return await service.clear_data()



# 同花顺-概念板块简介 - stock_board_concept_info_ths
@router.get("/collections/stock_board_concept_info_ths")
async def get_stock_board_concept_info_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-概念板块简介数据"""
    from app.services.stock.stock_board_concept_info_ths_service import StockBoardConceptInfoThsService
    service = StockBoardConceptInfoThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_info_ths/overview")
async def get_stock_board_concept_info_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-概念板块简介数据概览"""
    from app.services.stock.stock_board_concept_info_ths_service import StockBoardConceptInfoThsService
    service = StockBoardConceptInfoThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_info_ths/refresh")
async def refresh_stock_board_concept_info_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新同花顺-概念板块简介数据"""
    from app.services.stock.stock_board_concept_info_ths_service import StockBoardConceptInfoThsService
    service = StockBoardConceptInfoThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_info_ths/clear")
async def clear_stock_board_concept_info_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空同花顺-概念板块简介数据"""
    from app.services.stock.stock_board_concept_info_ths_service import StockBoardConceptInfoThsService
    service = StockBoardConceptInfoThsService(db)
    return await service.clear_data()



# 东方财富-概念板块 - stock_board_concept_name_em
@router.get("/collections/stock_board_concept_name_em")
async def get_stock_board_concept_name_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块数据"""
    from app.services.stock.stock_board_concept_name_em_service import StockBoardConceptNameEmService
    service = StockBoardConceptNameEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_name_em/overview")
async def get_stock_board_concept_name_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块数据概览"""
    from app.services.stock.stock_board_concept_name_em_service import StockBoardConceptNameEmService
    service = StockBoardConceptNameEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_name_em/refresh")
async def refresh_stock_board_concept_name_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-概念板块数据"""
    from app.services.stock.stock_board_concept_name_em_service import StockBoardConceptNameEmService
    service = StockBoardConceptNameEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_name_em/clear")
async def clear_stock_board_concept_name_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-概念板块数据"""
    from app.services.stock.stock_board_concept_name_em_service import StockBoardConceptNameEmService
    service = StockBoardConceptNameEmService(db)
    return await service.clear_data()



# 东方财富-概念板块-实时行情 - stock_board_concept_spot_em
@router.get("/collections/stock_board_concept_spot_em")
async def get_stock_board_concept_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_concept_spot_em/overview")
async def get_stock_board_concept_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-概念板块-实时行情数据概览"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_concept_spot_em/refresh")
async def refresh_stock_board_concept_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_concept_spot_em/clear")
async def clear_stock_board_concept_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-概念板块-实时行情数据"""
    from app.services.stock.stock_board_concept_spot_em_service import StockBoardConceptSpotEmService
    service = StockBoardConceptSpotEmService(db)
    return await service.clear_data()



# 东方财富-成份股 - stock_board_industry_cons_em
@router.get("/collections/stock_board_industry_cons_em")
async def get_stock_board_industry_cons_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据"""
    from app.services.stock.stock_board_industry_cons_em_service import StockBoardIndustryConsEmService
    service = StockBoardIndustryConsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_cons_em/overview")
async def get_stock_board_industry_cons_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-成份股数据概览"""
    from app.services.stock.stock_board_industry_cons_em_service import StockBoardIndustryConsEmService
    service = StockBoardIndustryConsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_cons_em/refresh")
async def refresh_stock_board_industry_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-成份股数据"""
    from app.services.stock.stock_board_industry_cons_em_service import StockBoardIndustryConsEmService
    service = StockBoardIndustryConsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_cons_em/clear")
async def clear_stock_board_industry_cons_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-成份股数据"""
    from app.services.stock.stock_board_industry_cons_em_service import StockBoardIndustryConsEmService
    service = StockBoardIndustryConsEmService(db)
    return await service.clear_data()



# 东方财富-指数-日频 - stock_board_industry_hist_em
@router.get("/collections/stock_board_industry_hist_em")
async def get_stock_board_industry_hist_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-日频数据"""
    from app.services.stock.stock_board_industry_hist_em_service import StockBoardIndustryHistEmService
    service = StockBoardIndustryHistEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_hist_em/overview")
async def get_stock_board_industry_hist_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-日频数据概览"""
    from app.services.stock.stock_board_industry_hist_em_service import StockBoardIndustryHistEmService
    service = StockBoardIndustryHistEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_hist_em/refresh")
async def refresh_stock_board_industry_hist_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-指数-日频数据"""
    from app.services.stock.stock_board_industry_hist_em_service import StockBoardIndustryHistEmService
    service = StockBoardIndustryHistEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_hist_em/clear")
async def clear_stock_board_industry_hist_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-指数-日频数据"""
    from app.services.stock.stock_board_industry_hist_em_service import StockBoardIndustryHistEmService
    service = StockBoardIndustryHistEmService(db)
    return await service.clear_data()



# 东方财富-指数-分时 - stock_board_industry_hist_min_em
@router.get("/collections/stock_board_industry_hist_min_em")
async def get_stock_board_industry_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-分时数据"""
    from app.services.stock.stock_board_industry_hist_min_em_service import StockBoardIndustryHistMinEmService
    service = StockBoardIndustryHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_hist_min_em/overview")
async def get_stock_board_industry_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-指数-分时数据概览"""
    from app.services.stock.stock_board_industry_hist_min_em_service import StockBoardIndustryHistMinEmService
    service = StockBoardIndustryHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_hist_min_em/refresh")
async def refresh_stock_board_industry_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-指数-分时数据"""
    from app.services.stock.stock_board_industry_hist_min_em_service import StockBoardIndustryHistMinEmService
    service = StockBoardIndustryHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_hist_min_em/clear")
async def clear_stock_board_industry_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-指数-分时数据"""
    from app.services.stock.stock_board_industry_hist_min_em_service import StockBoardIndustryHistMinEmService
    service = StockBoardIndustryHistMinEmService(db)
    return await service.clear_data()



# 同花顺-指数 - stock_board_industry_index_ths
@router.get("/collections/stock_board_industry_index_ths")
async def get_stock_board_industry_index_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_index_ths/overview")
async def get_stock_board_industry_index_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-指数数据概览"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_index_ths/refresh")
async def refresh_stock_board_industry_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_index_ths/clear")
async def clear_stock_board_industry_index_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空同花顺-指数数据"""
    from app.services.stock.stock_board_industry_index_ths_service import StockBoardIndustryIndexThsService
    service = StockBoardIndustryIndexThsService(db)
    return await service.clear_data()



# 东方财富-行业板块-实时行情 - stock_board_industry_spot_em
@router.get("/collections/stock_board_industry_spot_em")
async def get_stock_board_industry_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-行业板块-实时行情数据"""
    from app.services.stock.stock_board_industry_spot_em_service import StockBoardIndustrySpotEmService
    service = StockBoardIndustrySpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_spot_em/overview")
async def get_stock_board_industry_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取东方财富-行业板块-实时行情数据概览"""
    from app.services.stock.stock_board_industry_spot_em_service import StockBoardIndustrySpotEmService
    service = StockBoardIndustrySpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_spot_em/refresh")
async def refresh_stock_board_industry_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新东方财富-行业板块-实时行情数据"""
    from app.services.stock.stock_board_industry_spot_em_service import StockBoardIndustrySpotEmService
    service = StockBoardIndustrySpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_spot_em/clear")
async def clear_stock_board_industry_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空东方财富-行业板块-实时行情数据"""
    from app.services.stock.stock_board_industry_spot_em_service import StockBoardIndustrySpotEmService
    service = StockBoardIndustrySpotEmService(db)
    return await service.clear_data()



# 同花顺-同花顺行业一览表 - stock_board_industry_summary_ths
@router.get("/collections/stock_board_industry_summary_ths")
async def get_stock_board_industry_summary_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-同花顺行业一览表数据"""
    from app.services.stock.stock_board_industry_summary_ths_service import StockBoardIndustrySummaryThsService
    service = StockBoardIndustrySummaryThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_board_industry_summary_ths/overview")
async def get_stock_board_industry_summary_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取同花顺-同花顺行业一览表数据概览"""
    from app.services.stock.stock_board_industry_summary_ths_service import StockBoardIndustrySummaryThsService
    service = StockBoardIndustrySummaryThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_board_industry_summary_ths/refresh")
async def refresh_stock_board_industry_summary_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新同花顺-同花顺行业一览表数据"""
    from app.services.stock.stock_board_industry_summary_ths_service import StockBoardIndustrySummaryThsService
    service = StockBoardIndustrySummaryThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_board_industry_summary_ths/clear")
async def clear_stock_board_industry_summary_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空同花顺-同花顺行业一览表数据"""
    from app.services.stock.stock_board_industry_summary_ths_service import StockBoardIndustrySummaryThsService
    service = StockBoardIndustrySummaryThsService(db)
    return await service.clear_data()



# 巴菲特指标 - stock_buffett_index_lg
@router.get("/collections/stock_buffett_index_lg")
async def get_stock_buffett_index_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_buffett_index_lg/overview")
async def get_stock_buffett_index_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取巴菲特指标数据概览"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_buffett_index_lg/refresh")
async def refresh_stock_buffett_index_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_buffett_index_lg/clear")
async def clear_stock_buffett_index_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空巴菲特指标数据"""
    from app.services.stock.stock_buffett_index_lg_service import StockBuffettIndexLgService
    service = StockBuffettIndexLgService(db)
    return await service.clear_data()



# 股权质押 - stock_cg_equity_mortgage_cninfo
@router.get("/collections/stock_cg_equity_mortgage_cninfo")
async def get_stock_cg_equity_mortgage_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_equity_mortgage_cninfo/overview")
async def get_stock_cg_equity_mortgage_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股权质押数据概览"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_equity_mortgage_cninfo/refresh")
async def refresh_stock_cg_equity_mortgage_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_equity_mortgage_cninfo/clear")
async def clear_stock_cg_equity_mortgage_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股权质押数据"""
    from app.services.stock.stock_cg_equity_mortgage_cninfo_service import StockCgEquityMortgageCninfoService
    service = StockCgEquityMortgageCninfoService(db)
    return await service.clear_data()



# 对外担保 - stock_cg_guarantee_cninfo
@router.get("/collections/stock_cg_guarantee_cninfo")
async def get_stock_cg_guarantee_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_guarantee_cninfo/overview")
async def get_stock_cg_guarantee_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取对外担保数据概览"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_guarantee_cninfo/refresh")
async def refresh_stock_cg_guarantee_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_guarantee_cninfo/clear")
async def clear_stock_cg_guarantee_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空对外担保数据"""
    from app.services.stock.stock_cg_guarantee_cninfo_service import StockCgGuaranteeCninfoService
    service = StockCgGuaranteeCninfoService(db)
    return await service.clear_data()



# 公司诉讼 - stock_cg_lawsuit_cninfo
@router.get("/collections/stock_cg_lawsuit_cninfo")
async def get_stock_cg_lawsuit_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cg_lawsuit_cninfo/overview")
async def get_stock_cg_lawsuit_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司诉讼数据概览"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_cg_lawsuit_cninfo/refresh")
async def refresh_stock_cg_lawsuit_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cg_lawsuit_cninfo/clear")
async def clear_stock_cg_lawsuit_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司诉讼数据"""
    from app.services.stock.stock_cg_lawsuit_cninfo_service import StockCgLawsuitCninfoService
    service = StockCgLawsuitCninfoService(db)
    return await service.clear_data()



# 盘口异动 - stock_changes_em
@router.get("/collections/stock_changes_em")
async def get_stock_changes_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_changes_em/overview")
async def get_stock_changes_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘口异动数据概览"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_changes_em/refresh")
async def refresh_stock_changes_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_changes_em/clear")
async def clear_stock_changes_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盘口异动数据"""
    from app.services.stock.stock_changes_em_service import StockChangesEmService
    service = StockChangesEmService(db)
    return await service.clear_data()



# 流通股东 - stock_circulate_stock_holder
@router.get("/collections/stock_circulate_stock_holder")
async def get_stock_circulate_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_circulate_stock_holder/overview")
async def get_stock_circulate_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取流通股东数据概览"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_circulate_stock_holder/refresh")
async def refresh_stock_circulate_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_circulate_stock_holder/clear")
async def clear_stock_circulate_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空流通股东数据"""
    from app.services.stock.stock_circulate_stock_holder_service import StockCirculateStockHolderService
    service = StockCirculateStockHolderService(db)
    return await service.clear_data()



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



# 富途牛牛-美股概念-成分股 - stock_concept_cons_futu
@router.get("/collections/stock_concept_cons_futu")
async def get_stock_concept_cons_futu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_concept_cons_futu/overview")
async def get_stock_concept_cons_futu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取富途牛牛-美股概念-成分股数据概览"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.get_overview()


@router.post("/collections/stock_concept_cons_futu/refresh")
async def refresh_stock_concept_cons_futu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_concept_cons_futu/clear")
async def clear_stock_concept_cons_futu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空富途牛牛-美股概念-成分股数据"""
    from app.services.stock.stock_concept_cons_futu_service import StockConceptConsFutuService
    service = StockConceptConsFutuService(db)
    return await service.clear_data()



# 创业板 - stock_cy_a_spot_em
@router.get("/collections/stock_cy_a_spot_em")
async def get_stock_cy_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据"""
    from app.services.stock.stock_cy_a_spot_em_service import StockCyASpotEmService
    service = StockCyASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_cy_a_spot_em/overview")
async def get_stock_cy_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据概览"""
    from app.services.stock.stock_cy_a_spot_em_service import StockCyASpotEmService
    service = StockCyASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_cy_a_spot_em/refresh")
async def refresh_stock_cy_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新创业板数据"""
    from app.services.stock.stock_cy_a_spot_em_service import StockCyASpotEmService
    service = StockCyASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_cy_a_spot_em/clear")
async def clear_stock_cy_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空创业板数据"""
    from app.services.stock.stock_cy_a_spot_em_service import StockCyASpotEmService
    service = StockCyASpotEmService(db)
    return await service.clear_data()



# 历史分红 - stock_dividend_cninfo
@router.get("/collections/stock_dividend_cninfo")
async def get_stock_dividend_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dividend_cninfo/overview")
async def get_stock_dividend_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史分红数据概览"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_dividend_cninfo/refresh")
async def refresh_stock_dividend_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dividend_cninfo/clear")
async def clear_stock_dividend_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史分红数据"""
    from app.services.stock.stock_dividend_cninfo_service import StockDividendCninfoService
    service = StockDividendCninfoService(db)
    return await service.clear_data()



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



# 活跃 A 股统计 - stock_dzjy_hygtj
@router.get("/collections/stock_dzjy_hygtj")
async def get_stock_dzjy_hygtj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_hygtj/overview")
async def get_stock_dzjy_hygtj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃 A 股统计数据概览"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_hygtj/refresh")
async def refresh_stock_dzjy_hygtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_hygtj/clear")
async def clear_stock_dzjy_hygtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空活跃 A 股统计数据"""
    from app.services.stock.stock_dzjy_hygtj_service import StockDzjyHygtjService
    service = StockDzjyHygtjService(db)
    return await service.clear_data()



# 活跃营业部统计 - stock_dzjy_hyyybtj
@router.get("/collections/stock_dzjy_hyyybtj")
async def get_stock_dzjy_hyyybtj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_hyyybtj/overview")
async def get_stock_dzjy_hyyybtj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取活跃营业部统计数据概览"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_hyyybtj/refresh")
async def refresh_stock_dzjy_hyyybtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_hyyybtj/clear")
async def clear_stock_dzjy_hyyybtj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空活跃营业部统计数据"""
    from app.services.stock.stock_dzjy_hyyybtj_service import StockDzjyHyyybtjService
    service = StockDzjyHyyybtjService(db)
    return await service.clear_data()



# 营业部排行 - stock_dzjy_yybph
@router.get("/collections/stock_dzjy_yybph")
async def get_stock_dzjy_yybph(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_dzjy_yybph/overview")
async def get_stock_dzjy_yybph_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据概览"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.get_overview()


@router.post("/collections/stock_dzjy_yybph/refresh")
async def refresh_stock_dzjy_yybph(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_dzjy_yybph/clear")
async def clear_stock_dzjy_yybph(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部排行数据"""
    from app.services.stock.stock_dzjy_yybph_service import StockDzjyYybphService
    service = StockDzjyYybphService(db)
    return await service.clear_data()



# 股债利差 - stock_ebs_lg
@router.get("/collections/stock_ebs_lg")
async def get_stock_ebs_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ebs_lg/overview")
async def get_stock_ebs_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股债利差数据概览"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_ebs_lg/refresh")
async def refresh_stock_ebs_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ebs_lg/clear")
async def clear_stock_ebs_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股债利差数据"""
    from app.services.stock.stock_ebs_lg_service import StockEbsLgService
    service = StockEbsLgService(db)
    return await service.clear_data()



# 华证指数 - stock_esg_hz_sina
@router.get("/collections/stock_esg_hz_sina")
async def get_stock_esg_hz_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_hz_sina/overview")
async def get_stock_esg_hz_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取华证指数数据概览"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_hz_sina/refresh")
async def refresh_stock_esg_hz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_hz_sina/clear")
async def clear_stock_esg_hz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空华证指数数据"""
    from app.services.stock.stock_esg_hz_sina_service import StockEsgHzSinaService
    service = StockEsgHzSinaService(db)
    return await service.clear_data()



# MSCI - stock_esg_msci_sina
@router.get("/collections/stock_esg_msci_sina")
async def get_stock_esg_msci_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_msci_sina/overview")
async def get_stock_esg_msci_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取MSCI数据概览"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_msci_sina/refresh")
async def refresh_stock_esg_msci_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_msci_sina/clear")
async def clear_stock_esg_msci_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空MSCI数据"""
    from app.services.stock.stock_esg_msci_sina_service import StockEsgMsciSinaService
    service = StockEsgMsciSinaService(db)
    return await service.clear_data()



# ESG 评级数据 - stock_esg_rate_sina
@router.get("/collections/stock_esg_rate_sina")
async def get_stock_esg_rate_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取ESG 评级数据数据"""
    from app.services.stock.stock_esg_rate_sina_service import StockEsgRateSinaService
    service = StockEsgRateSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_rate_sina/overview")
async def get_stock_esg_rate_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取ESG 评级数据数据概览"""
    from app.services.stock.stock_esg_rate_sina_service import StockEsgRateSinaService
    service = StockEsgRateSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_rate_sina/refresh")
async def refresh_stock_esg_rate_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新ESG 评级数据数据"""
    from app.services.stock.stock_esg_rate_sina_service import StockEsgRateSinaService
    service = StockEsgRateSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_rate_sina/clear")
async def clear_stock_esg_rate_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空ESG 评级数据数据"""
    from app.services.stock.stock_esg_rate_sina_service import StockEsgRateSinaService
    service = StockEsgRateSinaService(db)
    return await service.clear_data()



# 路孚特 - stock_esg_rft_sina
@router.get("/collections/stock_esg_rft_sina")
async def get_stock_esg_rft_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_rft_sina/overview")
async def get_stock_esg_rft_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取路孚特数据概览"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_rft_sina/refresh")
async def refresh_stock_esg_rft_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_rft_sina/clear")
async def clear_stock_esg_rft_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空路孚特数据"""
    from app.services.stock.stock_esg_rft_sina_service import StockEsgRftSinaService
    service = StockEsgRftSinaService(db)
    return await service.clear_data()



# 秩鼎 - stock_esg_zd_sina
@router.get("/collections/stock_esg_zd_sina")
async def get_stock_esg_zd_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_esg_zd_sina/overview")
async def get_stock_esg_zd_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取秩鼎数据概览"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_esg_zd_sina/refresh")
async def refresh_stock_esg_zd_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_esg_zd_sina/clear")
async def clear_stock_esg_zd_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空秩鼎数据"""
    from app.services.stock.stock_esg_zd_sina_service import StockEsgZdSinaService
    service = StockEsgZdSinaService(db)
    return await service.clear_data()



# 分红配送详情-东财 - stock_fhps_detail_em
@router.get("/collections/stock_fhps_detail_em")
async def get_stock_fhps_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送详情-东财数据"""
    from app.services.stock.stock_fhps_detail_em_service import StockFhpsDetailEmService
    service = StockFhpsDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_fhps_detail_em/overview")
async def get_stock_fhps_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送详情-东财数据概览"""
    from app.services.stock.stock_fhps_detail_em_service import StockFhpsDetailEmService
    service = StockFhpsDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_fhps_detail_em/refresh")
async def refresh_stock_fhps_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红配送详情-东财数据"""
    from app.services.stock.stock_fhps_detail_em_service import StockFhpsDetailEmService
    service = StockFhpsDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_fhps_detail_em/clear")
async def clear_stock_fhps_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红配送详情-东财数据"""
    from app.services.stock.stock_fhps_detail_em_service import StockFhpsDetailEmService
    service = StockFhpsDetailEmService(db)
    return await service.clear_data()



# 分红配送-东财 - stock_fhps_em
@router.get("/collections/stock_fhps_em")
async def get_stock_fhps_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_fhps_em/overview")
async def get_stock_fhps_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配送-东财数据概览"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_fhps_em/refresh")
async def refresh_stock_fhps_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_fhps_em/clear")
async def clear_stock_fhps_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红配送-东财数据"""
    from app.services.stock.stock_fhps_em_service import StockFhpsEmService
    service = StockFhpsEmService(db)
    return await service.clear_data()



# 基金持股 - stock_fund_stock_holder
@router.get("/collections/stock_fund_stock_holder")
async def get_stock_fund_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_fund_stock_holder/overview")
async def get_stock_fund_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据概览"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_fund_stock_holder/refresh")
async def refresh_stock_fund_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_fund_stock_holder/clear")
async def clear_stock_fund_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股数据"""
    from app.services.stock.stock_fund_stock_holder_service import StockFundStockHolderService
    service = StockFundStockHolderService(db)
    return await service.clear_data()



# 股东持股明细-十大流通股东 - stock_gdfx_free_holding_detail_em
@router.get("/collections/stock_gdfx_free_holding_detail_em")
async def get_stock_gdfx_free_holding_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_detail_em_service import StockGdfxFreeHoldingDetailEmService
    service = StockGdfxFreeHoldingDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_free_holding_detail_em/overview")
async def get_stock_gdfx_free_holding_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大流通股东数据概览"""
    from app.services.stock.stock_gdfx_free_holding_detail_em_service import StockGdfxFreeHoldingDetailEmService
    service = StockGdfxFreeHoldingDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_free_holding_detail_em/refresh")
async def refresh_stock_gdfx_free_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东持股明细-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_detail_em_service import StockGdfxFreeHoldingDetailEmService
    service = StockGdfxFreeHoldingDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_free_holding_detail_em/clear")
async def clear_stock_gdfx_free_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东持股明细-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_detail_em_service import StockGdfxFreeHoldingDetailEmService
    service = StockGdfxFreeHoldingDetailEmService(db)
    return await service.clear_data()



# 股东持股统计-十大流通股东 - stock_gdfx_free_holding_statistics_em
@router.get("/collections/stock_gdfx_free_holding_statistics_em")
async def get_stock_gdfx_free_holding_statistics_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股统计-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_statistics_em_service import StockGdfxFreeHoldingStatisticsEmService
    service = StockGdfxFreeHoldingStatisticsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_free_holding_statistics_em/overview")
async def get_stock_gdfx_free_holding_statistics_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股统计-十大流通股东数据概览"""
    from app.services.stock.stock_gdfx_free_holding_statistics_em_service import StockGdfxFreeHoldingStatisticsEmService
    service = StockGdfxFreeHoldingStatisticsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_free_holding_statistics_em/refresh")
async def refresh_stock_gdfx_free_holding_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东持股统计-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_statistics_em_service import StockGdfxFreeHoldingStatisticsEmService
    service = StockGdfxFreeHoldingStatisticsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_free_holding_statistics_em/clear")
async def clear_stock_gdfx_free_holding_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东持股统计-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_statistics_em_service import StockGdfxFreeHoldingStatisticsEmService
    service = StockGdfxFreeHoldingStatisticsEmService(db)
    return await service.clear_data()



# 股东协同-十大流通股东 - stock_gdfx_free_holding_teamwork_em
@router.get("/collections/stock_gdfx_free_holding_teamwork_em")
async def get_stock_gdfx_free_holding_teamwork_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东协同-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_teamwork_em_service import StockGdfxFreeHoldingTeamworkEmService
    service = StockGdfxFreeHoldingTeamworkEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_free_holding_teamwork_em/overview")
async def get_stock_gdfx_free_holding_teamwork_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东协同-十大流通股东数据概览"""
    from app.services.stock.stock_gdfx_free_holding_teamwork_em_service import StockGdfxFreeHoldingTeamworkEmService
    service = StockGdfxFreeHoldingTeamworkEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_free_holding_teamwork_em/refresh")
async def refresh_stock_gdfx_free_holding_teamwork_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东协同-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_teamwork_em_service import StockGdfxFreeHoldingTeamworkEmService
    service = StockGdfxFreeHoldingTeamworkEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_free_holding_teamwork_em/clear")
async def clear_stock_gdfx_free_holding_teamwork_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东协同-十大流通股东数据"""
    from app.services.stock.stock_gdfx_free_holding_teamwork_em_service import StockGdfxFreeHoldingTeamworkEmService
    service = StockGdfxFreeHoldingTeamworkEmService(db)
    return await service.clear_data()



# 股东持股明细-十大股东 - stock_gdfx_holding_detail_em
@router.get("/collections/stock_gdfx_holding_detail_em")
async def get_stock_gdfx_holding_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_holding_detail_em/overview")
async def get_stock_gdfx_holding_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股明细-十大股东数据概览"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_holding_detail_em/refresh")
async def refresh_stock_gdfx_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_holding_detail_em/clear")
async def clear_stock_gdfx_holding_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东持股明细-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_detail_em_service import StockGdfxHoldingDetailEmService
    service = StockGdfxHoldingDetailEmService(db)
    return await service.clear_data()



# 股东持股统计-十大股东 - stock_gdfx_holding_statistics_em
@router.get("/collections/stock_gdfx_holding_statistics_em")
async def get_stock_gdfx_holding_statistics_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股统计-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_statistics_em_service import StockGdfxHoldingStatisticsEmService
    service = StockGdfxHoldingStatisticsEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_holding_statistics_em/overview")
async def get_stock_gdfx_holding_statistics_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东持股统计-十大股东数据概览"""
    from app.services.stock.stock_gdfx_holding_statistics_em_service import StockGdfxHoldingStatisticsEmService
    service = StockGdfxHoldingStatisticsEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_holding_statistics_em/refresh")
async def refresh_stock_gdfx_holding_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东持股统计-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_statistics_em_service import StockGdfxHoldingStatisticsEmService
    service = StockGdfxHoldingStatisticsEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_holding_statistics_em/clear")
async def clear_stock_gdfx_holding_statistics_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东持股统计-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_statistics_em_service import StockGdfxHoldingStatisticsEmService
    service = StockGdfxHoldingStatisticsEmService(db)
    return await service.clear_data()



# 股东协同-十大股东 - stock_gdfx_holding_teamwork_em
@router.get("/collections/stock_gdfx_holding_teamwork_em")
async def get_stock_gdfx_holding_teamwork_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东协同-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_teamwork_em_service import StockGdfxHoldingTeamworkEmService
    service = StockGdfxHoldingTeamworkEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gdfx_holding_teamwork_em/overview")
async def get_stock_gdfx_holding_teamwork_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东协同-十大股东数据概览"""
    from app.services.stock.stock_gdfx_holding_teamwork_em_service import StockGdfxHoldingTeamworkEmService
    service = StockGdfxHoldingTeamworkEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gdfx_holding_teamwork_em/refresh")
async def refresh_stock_gdfx_holding_teamwork_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东协同-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_teamwork_em_service import StockGdfxHoldingTeamworkEmService
    service = StockGdfxHoldingTeamworkEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gdfx_holding_teamwork_em/clear")
async def clear_stock_gdfx_holding_teamwork_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东协同-十大股东数据"""
    from app.services.stock.stock_gdfx_holding_teamwork_em_service import StockGdfxHoldingTeamworkEmService
    service = StockGdfxHoldingTeamworkEmService(db)
    return await service.clear_data()



# 股东增减持 - stock_ggcg_em
@router.get("/collections/stock_ggcg_em")
async def get_stock_ggcg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ggcg_em/overview")
async def get_stock_ggcg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东增减持数据概览"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_ggcg_em/refresh")
async def refresh_stock_ggcg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ggcg_em/clear")
async def clear_stock_ggcg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东增减持数据"""
    from app.services.stock.stock_ggcg_em_service import StockGgcgEmService
    service = StockGgcgEmService(db)
    return await service.clear_data()



# 质押机构分布统计-银行 - stock_gpzy_distribute_statistics_bank_em
@router.get("/collections/stock_gpzy_distribute_statistics_bank_em")
async def get_stock_gpzy_distribute_statistics_bank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_distribute_statistics_bank_em/overview")
async def get_stock_gpzy_distribute_statistics_bank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-银行数据概览"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_distribute_statistics_bank_em/refresh")
async def refresh_stock_gpzy_distribute_statistics_bank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_distribute_statistics_bank_em/clear")
async def clear_stock_gpzy_distribute_statistics_bank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空质押机构分布统计-银行数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_bank_em_service import StockGpzyDistributeStatisticsBankEmService
    service = StockGpzyDistributeStatisticsBankEmService(db)
    return await service.clear_data()



# 质押机构分布统计-证券公司 - stock_gpzy_distribute_statistics_company_em
@router.get("/collections/stock_gpzy_distribute_statistics_company_em")
async def get_stock_gpzy_distribute_statistics_company_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-证券公司数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_company_em_service import StockGpzyDistributeStatisticsCompanyEmService
    service = StockGpzyDistributeStatisticsCompanyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_distribute_statistics_company_em/overview")
async def get_stock_gpzy_distribute_statistics_company_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取质押机构分布统计-证券公司数据概览"""
    from app.services.stock.stock_gpzy_distribute_statistics_company_em_service import StockGpzyDistributeStatisticsCompanyEmService
    service = StockGpzyDistributeStatisticsCompanyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_distribute_statistics_company_em/refresh")
async def refresh_stock_gpzy_distribute_statistics_company_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新质押机构分布统计-证券公司数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_company_em_service import StockGpzyDistributeStatisticsCompanyEmService
    service = StockGpzyDistributeStatisticsCompanyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_distribute_statistics_company_em/clear")
async def clear_stock_gpzy_distribute_statistics_company_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空质押机构分布统计-证券公司数据"""
    from app.services.stock.stock_gpzy_distribute_statistics_company_em_service import StockGpzyDistributeStatisticsCompanyEmService
    service = StockGpzyDistributeStatisticsCompanyEmService(db)
    return await service.clear_data()



# 上市公司质押比例 - stock_gpzy_industry_data_em
@router.get("/collections/stock_gpzy_industry_data_em")
async def get_stock_gpzy_industry_data_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_industry_data_em_service import StockGpzyIndustryDataEmService
    service = StockGpzyIndustryDataEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_industry_data_em/overview")
async def get_stock_gpzy_industry_data_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据概览"""
    from app.services.stock.stock_gpzy_industry_data_em_service import StockGpzyIndustryDataEmService
    service = StockGpzyIndustryDataEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_industry_data_em/refresh")
async def refresh_stock_gpzy_industry_data_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_industry_data_em_service import StockGpzyIndustryDataEmService
    service = StockGpzyIndustryDataEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_industry_data_em/clear")
async def clear_stock_gpzy_industry_data_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_industry_data_em_service import StockGpzyIndustryDataEmService
    service = StockGpzyIndustryDataEmService(db)
    return await service.clear_data()



# 重要股东股权质押明细 - stock_gpzy_pledge_ratio_detail_em
@router.get("/collections/stock_gpzy_pledge_ratio_detail_em")
async def get_stock_gpzy_pledge_ratio_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取重要股东股权质押明细数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_detail_em_service import StockGpzyPledgeRatioDetailEmService
    service = StockGpzyPledgeRatioDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_pledge_ratio_detail_em/overview")
async def get_stock_gpzy_pledge_ratio_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取重要股东股权质押明细数据概览"""
    from app.services.stock.stock_gpzy_pledge_ratio_detail_em_service import StockGpzyPledgeRatioDetailEmService
    service = StockGpzyPledgeRatioDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_pledge_ratio_detail_em/refresh")
async def refresh_stock_gpzy_pledge_ratio_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新重要股东股权质押明细数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_detail_em_service import StockGpzyPledgeRatioDetailEmService
    service = StockGpzyPledgeRatioDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_pledge_ratio_detail_em/clear")
async def clear_stock_gpzy_pledge_ratio_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空重要股东股权质押明细数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_detail_em_service import StockGpzyPledgeRatioDetailEmService
    service = StockGpzyPledgeRatioDetailEmService(db)
    return await service.clear_data()



# 上市公司质押比例 - stock_gpzy_pledge_ratio_em
@router.get("/collections/stock_gpzy_pledge_ratio_em")
async def get_stock_gpzy_pledge_ratio_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gpzy_pledge_ratio_em/overview")
async def get_stock_gpzy_pledge_ratio_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司质押比例数据概览"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gpzy_pledge_ratio_em/refresh")
async def refresh_stock_gpzy_pledge_ratio_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gpzy_pledge_ratio_em/clear")
async def clear_stock_gpzy_pledge_ratio_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市公司质押比例数据"""
    from app.services.stock.stock_gpzy_pledge_ratio_em_service import StockGpzyPledgeRatioEmService
    service = StockGpzyPledgeRatioEmService(db)
    return await service.clear_data()



# 公司动态 - stock_gsrl_gsdt_em
@router.get("/collections/stock_gsrl_gsdt_em")
async def get_stock_gsrl_gsdt_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_gsrl_gsdt_em/overview")
async def get_stock_gsrl_gsdt_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司动态数据概览"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_gsrl_gsdt_em/refresh")
async def refresh_stock_gsrl_gsdt_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_gsrl_gsdt_em/clear")
async def clear_stock_gsrl_gsdt_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司动态数据"""
    from app.services.stock.stock_gsrl_gsdt_em_service import StockGsrlGsdtEmService
    service = StockGsrlGsdtEmService(db)
    return await service.clear_data()



# 分红配股 - stock_history_dividend_detail
@router.get("/collections/stock_history_dividend_detail")
async def get_stock_history_dividend_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_history_dividend_detail/overview")
async def get_stock_history_dividend_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红配股数据概览"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_history_dividend_detail/refresh")
async def refresh_stock_history_dividend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_history_dividend_detail/clear")
async def clear_stock_history_dividend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红配股数据"""
    from app.services.stock.stock_history_dividend_detail_service import StockHistoryDividendDetailService
    service = StockHistoryDividendDetailService(db)
    return await service.clear_data()



# 公司资料 - stock_hk_company_profile_em
@router.get("/collections/stock_hk_company_profile_em")
async def get_stock_hk_company_profile_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_company_profile_em/overview")
async def get_stock_hk_company_profile_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司资料数据概览"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_company_profile_em/refresh")
async def refresh_stock_hk_company_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_company_profile_em/clear")
async def clear_stock_hk_company_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司资料数据"""
    from app.services.stock.stock_hk_company_profile_em_service import StockHkCompanyProfileEmService
    service = StockHkCompanyProfileEmService(db)
    return await service.clear_data()



# 历史行情数据-新浪 - stock_hk_daily
@router.get("/collections/stock_hk_daily")
async def get_stock_hk_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_daily/overview")
async def get_stock_hk_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据概览"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_daily/refresh")
async def refresh_stock_hk_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_daily/clear")
async def clear_stock_hk_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-新浪数据"""
    from app.services.stock.stock_hk_daily_service import StockHkDailyService
    service = StockHkDailyService(db)
    return await service.clear_data()



# 分红派息 - stock_hk_dividend_payout_em
@router.get("/collections/stock_hk_dividend_payout_em")
async def get_stock_hk_dividend_payout_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_dividend_payout_em/overview")
async def get_stock_hk_dividend_payout_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分红派息数据概览"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_dividend_payout_em/refresh")
async def refresh_stock_hk_dividend_payout_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_dividend_payout_em/clear")
async def clear_stock_hk_dividend_payout_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分红派息数据"""
    from app.services.stock.stock_hk_dividend_payout_em_service import StockHkDividendPayoutEmService
    service = StockHkDividendPayoutEmService(db)
    return await service.clear_data()



# 知名港股 - stock_hk_famous_spot_em
@router.get("/collections/stock_hk_famous_spot_em")
async def get_stock_hk_famous_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取知名港股数据"""
    from app.services.stock.stock_hk_famous_spot_em_service import StockHkFamousSpotEmService
    service = StockHkFamousSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_famous_spot_em/overview")
async def get_stock_hk_famous_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取知名港股数据概览"""
    from app.services.stock.stock_hk_famous_spot_em_service import StockHkFamousSpotEmService
    service = StockHkFamousSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_famous_spot_em/refresh")
async def refresh_stock_hk_famous_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新知名港股数据"""
    from app.services.stock.stock_hk_famous_spot_em_service import StockHkFamousSpotEmService
    service = StockHkFamousSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_famous_spot_em/clear")
async def clear_stock_hk_famous_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空知名港股数据"""
    from app.services.stock.stock_hk_famous_spot_em_service import StockHkFamousSpotEmService
    service = StockHkFamousSpotEmService(db)
    return await service.clear_data()



# 财务指标 - stock_hk_financial_indicator_em
@router.get("/collections/stock_hk_financial_indicator_em")
async def get_stock_hk_financial_indicator_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_financial_indicator_em/overview")
async def get_stock_hk_financial_indicator_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财务指标数据概览"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_financial_indicator_em/refresh")
async def refresh_stock_hk_financial_indicator_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_financial_indicator_em/clear")
async def clear_stock_hk_financial_indicator_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财务指标数据"""
    from app.services.stock.stock_hk_financial_indicator_em_service import StockHkFinancialIndicatorEmService
    service = StockHkFinancialIndicatorEmService(db)
    return await service.clear_data()



# 成长性对比 - stock_hk_growth_comparison_em
@router.get("/collections/stock_hk_growth_comparison_em")
async def get_stock_hk_growth_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取成长性对比数据"""
    from app.services.stock.stock_hk_growth_comparison_em_service import StockHkGrowthComparisonEmService
    service = StockHkGrowthComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_growth_comparison_em/overview")
async def get_stock_hk_growth_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取成长性对比数据概览"""
    from app.services.stock.stock_hk_growth_comparison_em_service import StockHkGrowthComparisonEmService
    service = StockHkGrowthComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_growth_comparison_em/refresh")
async def refresh_stock_hk_growth_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新成长性对比数据"""
    from app.services.stock.stock_hk_growth_comparison_em_service import StockHkGrowthComparisonEmService
    service = StockHkGrowthComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_growth_comparison_em/clear")
async def clear_stock_hk_growth_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空成长性对比数据"""
    from app.services.stock.stock_hk_growth_comparison_em_service import StockHkGrowthComparisonEmService
    service = StockHkGrowthComparisonEmService(db)
    return await service.clear_data()



# 恒生指数股息率 - stock_hk_gxl_lg
@router.get("/collections/stock_hk_gxl_lg")
async def get_stock_hk_gxl_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_gxl_lg/overview")
async def get_stock_hk_gxl_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取恒生指数股息率数据概览"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_gxl_lg/refresh")
async def refresh_stock_hk_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_gxl_lg/clear")
async def clear_stock_hk_gxl_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空恒生指数股息率数据"""
    from app.services.stock.stock_hk_gxl_lg_service import StockHkGxlLgService
    service = StockHkGxlLgService(db)
    return await service.clear_data()



# 历史行情数据-东财 - stock_hk_hist
@router.get("/collections/stock_hk_hist")
async def get_stock_hk_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hist/overview")
async def get_stock_hk_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据概览"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hist/refresh")
async def refresh_stock_hk_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hist/clear")
async def clear_stock_hk_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-东财数据"""
    from app.services.stock.stock_hk_hist_service import StockHkHistService
    service = StockHkHistService(db)
    return await service.clear_data()



# 分时数据-东财 - stock_hk_hist_min_em
@router.get("/collections/stock_hk_hist_min_em")
async def get_stock_hk_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据"""
    from app.services.stock.stock_hk_hist_min_em_service import StockHkHistMinEmService
    service = StockHkHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hist_min_em/overview")
async def get_stock_hk_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据概览"""
    from app.services.stock.stock_hk_hist_min_em_service import StockHkHistMinEmService
    service = StockHkHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hist_min_em/refresh")
async def refresh_stock_hk_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据-东财数据"""
    from app.services.stock.stock_hk_hist_min_em_service import StockHkHistMinEmService
    service = StockHkHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hist_min_em/clear")
async def clear_stock_hk_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据-东财数据"""
    from app.services.stock.stock_hk_hist_min_em_service import StockHkHistMinEmService
    service = StockHkHistMinEmService(db)
    return await service.clear_data()



# 港股 - stock_hk_hot_rank_detail_em
@router.get("/collections/stock_hk_hot_rank_detail_em")
async def get_stock_hk_hot_rank_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_em_service import StockHkHotRankDetailEmService
    service = StockHkHotRankDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hot_rank_detail_em/overview")
async def get_stock_hk_hot_rank_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据概览"""
    from app.services.stock.stock_hk_hot_rank_detail_em_service import StockHkHotRankDetailEmService
    service = StockHkHotRankDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hot_rank_detail_em/refresh")
async def refresh_stock_hk_hot_rank_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_em_service import StockHkHotRankDetailEmService
    service = StockHkHotRankDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hot_rank_detail_em/clear")
async def clear_stock_hk_hot_rank_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_em_service import StockHkHotRankDetailEmService
    service = StockHkHotRankDetailEmService(db)
    return await service.clear_data()



# 港股 - stock_hk_hot_rank_detail_realtime_em
@router.get("/collections/stock_hk_hot_rank_detail_realtime_em")
async def get_stock_hk_hot_rank_detail_realtime_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hot_rank_detail_realtime_em/overview")
async def get_stock_hk_hot_rank_detail_realtime_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据概览"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hot_rank_detail_realtime_em/refresh")
async def refresh_stock_hk_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hot_rank_detail_realtime_em/clear")
async def clear_stock_hk_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股数据"""
    from app.services.stock.stock_hk_hot_rank_detail_realtime_em_service import StockHkHotRankDetailRealtimeEmService
    service = StockHkHotRankDetailRealtimeEmService(db)
    return await service.clear_data()



# 人气榜-港股 - stock_hk_hot_rank_em
@router.get("/collections/stock_hk_hot_rank_em")
async def get_stock_hk_hot_rank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-港股数据"""
    from app.services.stock.stock_hk_hot_rank_em_service import StockHkHotRankEmService
    service = StockHkHotRankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hot_rank_em/overview")
async def get_stock_hk_hot_rank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-港股数据概览"""
    from app.services.stock.stock_hk_hot_rank_em_service import StockHkHotRankEmService
    service = StockHkHotRankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hot_rank_em/refresh")
async def refresh_stock_hk_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新人气榜-港股数据"""
    from app.services.stock.stock_hk_hot_rank_em_service import StockHkHotRankEmService
    service = StockHkHotRankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hot_rank_em/clear")
async def clear_stock_hk_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空人气榜-港股数据"""
    from app.services.stock.stock_hk_hot_rank_em_service import StockHkHotRankEmService
    service = StockHkHotRankEmService(db)
    return await service.clear_data()



# 港股 - stock_hk_hot_rank_latest_em
@router.get("/collections/stock_hk_hot_rank_latest_em")
async def get_stock_hk_hot_rank_latest_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据"""
    from app.services.stock.stock_hk_hot_rank_latest_em_service import StockHkHotRankLatestEmService
    service = StockHkHotRankLatestEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_hot_rank_latest_em/overview")
async def get_stock_hk_hot_rank_latest_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股数据概览"""
    from app.services.stock.stock_hk_hot_rank_latest_em_service import StockHkHotRankLatestEmService
    service = StockHkHotRankLatestEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_hot_rank_latest_em/refresh")
async def refresh_stock_hk_hot_rank_latest_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股数据"""
    from app.services.stock.stock_hk_hot_rank_latest_em_service import StockHkHotRankLatestEmService
    service = StockHkHotRankLatestEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_hot_rank_latest_em/clear")
async def clear_stock_hk_hot_rank_latest_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股数据"""
    from app.services.stock.stock_hk_hot_rank_latest_em_service import StockHkHotRankLatestEmService
    service = StockHkHotRankLatestEmService(db)
    return await service.clear_data()



# 港股个股指标 - stock_hk_indicator_eniu
@router.get("/collections/stock_hk_indicator_eniu")
async def get_stock_hk_indicator_eniu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_indicator_eniu/overview")
async def get_stock_hk_indicator_eniu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股个股指标数据概览"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_indicator_eniu/refresh")
async def refresh_stock_hk_indicator_eniu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_indicator_eniu/clear")
async def clear_stock_hk_indicator_eniu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股个股指标数据"""
    from app.services.stock.stock_hk_indicator_eniu_service import StockHkIndicatorEniuService
    service = StockHkIndicatorEniuService(db)
    return await service.clear_data()



# 港股主板实时行情数据-东财 - stock_hk_main_board_spot_em
@router.get("/collections/stock_hk_main_board_spot_em")
async def get_stock_hk_main_board_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股主板实时行情数据-东财数据"""
    from app.services.stock.stock_hk_main_board_spot_em_service import StockHkMainBoardSpotEmService
    service = StockHkMainBoardSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_main_board_spot_em/overview")
async def get_stock_hk_main_board_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股主板实时行情数据-东财数据概览"""
    from app.services.stock.stock_hk_main_board_spot_em_service import StockHkMainBoardSpotEmService
    service = StockHkMainBoardSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_main_board_spot_em/refresh")
async def refresh_stock_hk_main_board_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股主板实时行情数据-东财数据"""
    from app.services.stock.stock_hk_main_board_spot_em_service import StockHkMainBoardSpotEmService
    service = StockHkMainBoardSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_main_board_spot_em/clear")
async def clear_stock_hk_main_board_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股主板实时行情数据-东财数据"""
    from app.services.stock.stock_hk_main_board_spot_em_service import StockHkMainBoardSpotEmService
    service = StockHkMainBoardSpotEmService(db)
    return await service.clear_data()



# 港股盈利预测-经济通 - stock_hk_profit_forecast_et
@router.get("/collections/stock_hk_profit_forecast_et")
async def get_stock_hk_profit_forecast_et(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_profit_forecast_et/overview")
async def get_stock_hk_profit_forecast_et_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股盈利预测-经济通数据概览"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_profit_forecast_et/refresh")
async def refresh_stock_hk_profit_forecast_et(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_profit_forecast_et/clear")
async def clear_stock_hk_profit_forecast_et(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股盈利预测-经济通数据"""
    from app.services.stock.stock_hk_profit_forecast_et_service import StockHkProfitForecastEtService
    service = StockHkProfitForecastEtService(db)
    return await service.clear_data()



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



# 证券资料 - stock_hk_security_profile_em
@router.get("/collections/stock_hk_security_profile_em")
async def get_stock_hk_security_profile_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券资料数据"""
    from app.services.stock.stock_hk_security_profile_em_service import StockHkSecurityProfileEmService
    service = StockHkSecurityProfileEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_security_profile_em/overview")
async def get_stock_hk_security_profile_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券资料数据概览"""
    from app.services.stock.stock_hk_security_profile_em_service import StockHkSecurityProfileEmService
    service = StockHkSecurityProfileEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_security_profile_em/refresh")
async def refresh_stock_hk_security_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新证券资料数据"""
    from app.services.stock.stock_hk_security_profile_em_service import StockHkSecurityProfileEmService
    service = StockHkSecurityProfileEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_security_profile_em/clear")
async def clear_stock_hk_security_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空证券资料数据"""
    from app.services.stock.stock_hk_security_profile_em_service import StockHkSecurityProfileEmService
    service = StockHkSecurityProfileEmService(db)
    return await service.clear_data()



# 实时行情数据-新浪 - stock_hk_spot
@router.get("/collections/stock_hk_spot")
async def get_stock_hk_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据"""
    from app.services.stock.stock_hk_spot_service import StockHkSpotService
    service = StockHkSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_spot/overview")
async def get_stock_hk_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据概览"""
    from app.services.stock.stock_hk_spot_service import StockHkSpotService
    service = StockHkSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_spot/refresh")
async def refresh_stock_hk_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-新浪数据"""
    from app.services.stock.stock_hk_spot_service import StockHkSpotService
    service = StockHkSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_spot/clear")
async def clear_stock_hk_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-新浪数据"""
    from app.services.stock.stock_hk_spot_service import StockHkSpotService
    service = StockHkSpotService(db)
    return await service.clear_data()



# 实时行情数据-东财 - stock_hk_spot_em
@router.get("/collections/stock_hk_spot_em")
async def get_stock_hk_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据"""
    from app.services.stock.stock_hk_spot_em_service import StockHkSpotEmService
    service = StockHkSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_spot_em/overview")
async def get_stock_hk_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据概览"""
    from app.services.stock.stock_hk_spot_em_service import StockHkSpotEmService
    service = StockHkSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_spot_em/refresh")
async def refresh_stock_hk_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-东财数据"""
    from app.services.stock.stock_hk_spot_em_service import StockHkSpotEmService
    service = StockHkSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_spot_em/clear")
async def clear_stock_hk_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-东财数据"""
    from app.services.stock.stock_hk_spot_em_service import StockHkSpotEmService
    service = StockHkSpotEmService(db)
    return await service.clear_data()



# 港股估值指标 - stock_hk_valuation_baidu
@router.get("/collections/stock_hk_valuation_baidu")
async def get_stock_hk_valuation_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_valuation_baidu/overview")
async def get_stock_hk_valuation_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取港股估值指标数据概览"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_valuation_baidu/refresh")
async def refresh_stock_hk_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_valuation_baidu/clear")
async def clear_stock_hk_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空港股估值指标数据"""
    from app.services.stock.stock_hk_valuation_baidu_service import StockHkValuationBaiduService
    service = StockHkValuationBaiduService(db)
    return await service.clear_data()



# 估值对比 - stock_hk_valuation_comparison_em
@router.get("/collections/stock_hk_valuation_comparison_em")
async def get_stock_hk_valuation_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值对比数据"""
    from app.services.stock.stock_hk_valuation_comparison_em_service import StockHkValuationComparisonEmService
    service = StockHkValuationComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hk_valuation_comparison_em/overview")
async def get_stock_hk_valuation_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值对比数据概览"""
    from app.services.stock.stock_hk_valuation_comparison_em_service import StockHkValuationComparisonEmService
    service = StockHkValuationComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hk_valuation_comparison_em/refresh")
async def refresh_stock_hk_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新估值对比数据"""
    from app.services.stock.stock_hk_valuation_comparison_em_service import StockHkValuationComparisonEmService
    service = StockHkValuationComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hk_valuation_comparison_em/clear")
async def clear_stock_hk_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空估值对比数据"""
    from app.services.stock.stock_hk_valuation_comparison_em_service import StockHkValuationComparisonEmService
    service = StockHkValuationComparisonEmService(db)
    return await service.clear_data()



# 股本变动 - stock_hold_change_cninfo
@router.get("/collections/stock_hold_change_cninfo")
async def get_stock_hold_change_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_change_cninfo/overview")
async def get_stock_hold_change_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本变动数据概览"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_change_cninfo/refresh")
async def refresh_stock_hold_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_change_cninfo/clear")
async def clear_stock_hold_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股本变动数据"""
    from app.services.stock.stock_hold_change_cninfo_service import StockHoldChangeCninfoService
    service = StockHoldChangeCninfoService(db)
    return await service.clear_data()



# 实际控制人持股变动 - stock_hold_control_cninfo
@router.get("/collections/stock_hold_control_cninfo")
async def get_stock_hold_control_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_control_cninfo/overview")
async def get_stock_hold_control_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实际控制人持股变动数据概览"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_control_cninfo/refresh")
async def refresh_stock_hold_control_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_control_cninfo/clear")
async def clear_stock_hold_control_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实际控制人持股变动数据"""
    from app.services.stock.stock_hold_control_cninfo_service import StockHoldControlCninfoService
    service = StockHoldControlCninfoService(db)
    return await service.clear_data()



# 高管持股变动明细 - stock_hold_management_detail_cninfo
@router.get("/collections/stock_hold_management_detail_cninfo")
async def get_stock_hold_management_detail_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_detail_cninfo/overview")
async def get_stock_hold_management_detail_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取高管持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_detail_cninfo/refresh")
async def refresh_stock_hold_management_detail_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_detail_cninfo/clear")
async def clear_stock_hold_management_detail_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空高管持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_cninfo_service import StockHoldManagementDetailCninfoService
    service = StockHoldManagementDetailCninfoService(db)
    return await service.clear_data()



# 董监高及相关人员持股变动明细 - stock_hold_management_detail_em
@router.get("/collections/stock_hold_management_detail_em")
async def get_stock_hold_management_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_detail_em/overview")
async def get_stock_hold_management_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_detail_em/refresh")
async def refresh_stock_hold_management_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_detail_em/clear")
async def clear_stock_hold_management_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动明细数据"""
    from app.services.stock.stock_hold_management_detail_em_service import StockHoldManagementDetailEmService
    service = StockHoldManagementDetailEmService(db)
    return await service.clear_data()



# 人员增减持股变动明细 - stock_hold_management_person_em
@router.get("/collections/stock_hold_management_person_em")
async def get_stock_hold_management_person_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_management_person_em/overview")
async def get_stock_hold_management_person_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人员增减持股变动明细数据概览"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_management_person_em/refresh")
async def refresh_stock_hold_management_person_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_management_person_em/clear")
async def clear_stock_hold_management_person_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空人员增减持股变动明细数据"""
    from app.services.stock.stock_hold_management_person_em_service import StockHoldManagementPersonEmService
    service = StockHoldManagementPersonEmService(db)
    return await service.clear_data()



# 股东人数及持股集中度 - stock_hold_num_cninfo
@router.get("/collections/stock_hold_num_cninfo")
async def get_stock_hold_num_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hold_num_cninfo/overview")
async def get_stock_hold_num_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东人数及持股集中度数据概览"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_hold_num_cninfo/refresh")
async def refresh_stock_hold_num_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hold_num_cninfo/clear")
async def clear_stock_hold_num_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东人数及持股集中度数据"""
    from app.services.stock.stock_hold_num_cninfo_service import StockHoldNumCninfoService
    service = StockHoldNumCninfoService(db)
    return await service.clear_data()



# 交易排行榜 - stock_hot_deal_xq
@router.get("/collections/stock_hot_deal_xq")
async def get_stock_hot_deal_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_deal_xq/overview")
async def get_stock_hot_deal_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取交易排行榜数据概览"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_deal_xq/refresh")
async def refresh_stock_hot_deal_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_deal_xq/clear")
async def clear_stock_hot_deal_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空交易排行榜数据"""
    from app.services.stock.stock_hot_deal_xq_service import StockHotDealXqService
    service = StockHotDealXqService(db)
    return await service.clear_data()



# 关注排行榜 - stock_hot_follow_xq
@router.get("/collections/stock_hot_follow_xq")
async def get_stock_hot_follow_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_follow_xq/overview")
async def get_stock_hot_follow_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取关注排行榜数据概览"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_follow_xq/refresh")
async def refresh_stock_hot_follow_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_follow_xq/clear")
async def clear_stock_hot_follow_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空关注排行榜数据"""
    from app.services.stock.stock_hot_follow_xq_service import StockHotFollowXqService
    service = StockHotFollowXqService(db)
    return await service.clear_data()



# 热门关键词 - stock_hot_keyword_em
@router.get("/collections/stock_hot_keyword_em")
async def get_stock_hot_keyword_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_keyword_em/overview")
async def get_stock_hot_keyword_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热门关键词数据概览"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_keyword_em/refresh")
async def refresh_stock_hot_keyword_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_keyword_em/clear")
async def clear_stock_hot_keyword_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空热门关键词数据"""
    from app.services.stock.stock_hot_keyword_em_service import StockHotKeywordEmService
    service = StockHotKeywordEmService(db)
    return await service.clear_data()



# A股 - stock_hot_rank_detail_em
@router.get("/collections/stock_hot_rank_detail_em")
async def get_stock_hot_rank_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据"""
    from app.services.stock.stock_hot_rank_detail_em_service import StockHotRankDetailEmService
    service = StockHotRankDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_detail_em/overview")
async def get_stock_hot_rank_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据概览"""
    from app.services.stock.stock_hot_rank_detail_em_service import StockHotRankDetailEmService
    service = StockHotRankDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_detail_em/refresh")
async def refresh_stock_hot_rank_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股数据"""
    from app.services.stock.stock_hot_rank_detail_em_service import StockHotRankDetailEmService
    service = StockHotRankDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_detail_em/clear")
async def clear_stock_hot_rank_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股数据"""
    from app.services.stock.stock_hot_rank_detail_em_service import StockHotRankDetailEmService
    service = StockHotRankDetailEmService(db)
    return await service.clear_data()



# A股 - stock_hot_rank_detail_realtime_em
@router.get("/collections/stock_hot_rank_detail_realtime_em")
async def get_stock_hot_rank_detail_realtime_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据"""
    from app.services.stock.stock_hot_rank_detail_realtime_em_service import StockHotRankDetailRealtimeEmService
    service = StockHotRankDetailRealtimeEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_detail_realtime_em/overview")
async def get_stock_hot_rank_detail_realtime_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据概览"""
    from app.services.stock.stock_hot_rank_detail_realtime_em_service import StockHotRankDetailRealtimeEmService
    service = StockHotRankDetailRealtimeEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_detail_realtime_em/refresh")
async def refresh_stock_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股数据"""
    from app.services.stock.stock_hot_rank_detail_realtime_em_service import StockHotRankDetailRealtimeEmService
    service = StockHotRankDetailRealtimeEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_detail_realtime_em/clear")
async def clear_stock_hot_rank_detail_realtime_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股数据"""
    from app.services.stock.stock_hot_rank_detail_realtime_em_service import StockHotRankDetailRealtimeEmService
    service = StockHotRankDetailRealtimeEmService(db)
    return await service.clear_data()



# 人气榜-A股 - stock_hot_rank_em
@router.get("/collections/stock_hot_rank_em")
async def get_stock_hot_rank_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_em/overview")
async def get_stock_hot_rank_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取人气榜-A股数据概览"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_em/refresh")
async def refresh_stock_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_em/clear")
async def clear_stock_hot_rank_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空人气榜-A股数据"""
    from app.services.stock.stock_hot_rank_em_service import StockHotRankEmService
    service = StockHotRankEmService(db)
    return await service.clear_data()



# A股 - stock_hot_rank_latest_em
@router.get("/collections/stock_hot_rank_latest_em")
async def get_stock_hot_rank_latest_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据"""
    from app.services.stock.stock_hot_rank_latest_em_service import StockHotRankLatestEmService
    service = StockHotRankLatestEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_latest_em/overview")
async def get_stock_hot_rank_latest_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股数据概览"""
    from app.services.stock.stock_hot_rank_latest_em_service import StockHotRankLatestEmService
    service = StockHotRankLatestEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_latest_em/refresh")
async def refresh_stock_hot_rank_latest_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股数据"""
    from app.services.stock.stock_hot_rank_latest_em_service import StockHotRankLatestEmService
    service = StockHotRankLatestEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_latest_em/clear")
async def clear_stock_hot_rank_latest_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股数据"""
    from app.services.stock.stock_hot_rank_latest_em_service import StockHotRankLatestEmService
    service = StockHotRankLatestEmService(db)
    return await service.clear_data()



# 相关股票 - stock_hot_rank_relate_em
@router.get("/collections/stock_hot_rank_relate_em")
async def get_stock_hot_rank_relate_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取相关股票数据"""
    from app.services.stock.stock_hot_rank_relate_em_service import StockHotRankRelateEmService
    service = StockHotRankRelateEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_rank_relate_em/overview")
async def get_stock_hot_rank_relate_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取相关股票数据概览"""
    from app.services.stock.stock_hot_rank_relate_em_service import StockHotRankRelateEmService
    service = StockHotRankRelateEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_rank_relate_em/refresh")
async def refresh_stock_hot_rank_relate_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新相关股票数据"""
    from app.services.stock.stock_hot_rank_relate_em_service import StockHotRankRelateEmService
    service = StockHotRankRelateEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_rank_relate_em/clear")
async def clear_stock_hot_rank_relate_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空相关股票数据"""
    from app.services.stock.stock_hot_rank_relate_em_service import StockHotRankRelateEmService
    service = StockHotRankRelateEmService(db)
    return await service.clear_data()



# 热搜股票 - stock_hot_search_baidu
@router.get("/collections/stock_hot_search_baidu")
async def get_stock_hot_search_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_search_baidu/overview")
async def get_stock_hot_search_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取热搜股票数据概览"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_search_baidu/refresh")
async def refresh_stock_hot_search_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_search_baidu/clear")
async def clear_stock_hot_search_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空热搜股票数据"""
    from app.services.stock.stock_hot_search_baidu_service import StockHotSearchBaiduService
    service = StockHotSearchBaiduService(db)
    return await service.clear_data()



# 讨论排行榜 - stock_hot_tweet_xq
@router.get("/collections/stock_hot_tweet_xq")
async def get_stock_hot_tweet_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_tweet_xq/overview")
async def get_stock_hot_tweet_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取讨论排行榜数据概览"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_tweet_xq/refresh")
async def refresh_stock_hot_tweet_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_tweet_xq/clear")
async def clear_stock_hot_tweet_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空讨论排行榜数据"""
    from app.services.stock.stock_hot_tweet_xq_service import StockHotTweetXqService
    service = StockHotTweetXqService(db)
    return await service.clear_data()



# 飙升榜-A股 - stock_hot_up_em
@router.get("/collections/stock_hot_up_em")
async def get_stock_hot_up_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hot_up_em/overview")
async def get_stock_hot_up_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取飙升榜-A股数据概览"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hot_up_em/refresh")
async def refresh_stock_hot_up_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hot_up_em/clear")
async def clear_stock_hot_up_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空飙升榜-A股数据"""
    from app.services.stock.stock_hot_up_em_service import StockHotUpEmService
    service = StockHotUpEmService(db)
    return await service.clear_data()



# 沪深港通资金流向 - stock_hsgt_fund_flow_summary_em
@router.get("/collections/stock_hsgt_fund_flow_summary_em")
async def get_stock_hsgt_fund_flow_summary_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_hsgt_fund_flow_summary_em/overview")
async def get_stock_hsgt_fund_flow_summary_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深港通资金流向数据概览"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_hsgt_fund_flow_summary_em/refresh")
async def refresh_stock_hsgt_fund_flow_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_hsgt_fund_flow_summary_em/clear")
async def clear_stock_hsgt_fund_flow_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪深港通资金流向数据"""
    from app.services.stock.stock_hsgt_fund_flow_summary_em_service import StockHsgtFundFlowSummaryEmService
    service = StockHsgtFundFlowSummaryEmService(db)
    return await service.clear_data()



# 指数市净率 - stock_index_pb_lg
@router.get("/collections/stock_index_pb_lg")
async def get_stock_index_pb_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_index_pb_lg/overview")
async def get_stock_index_pb_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市净率数据概览"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_index_pb_lg/refresh")
async def refresh_stock_index_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_index_pb_lg/clear")
async def clear_stock_index_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空指数市净率数据"""
    from app.services.stock.stock_index_pb_lg_service import StockIndexPbLgService
    service = StockIndexPbLgService(db)
    return await service.clear_data()



# 指数市盈率 - stock_index_pe_lg
@router.get("/collections/stock_index_pe_lg")
async def get_stock_index_pe_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市盈率数据"""
    from app.services.stock.stock_index_pe_lg_service import StockIndexPeLgService
    service = StockIndexPeLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_index_pe_lg/overview")
async def get_stock_index_pe_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取指数市盈率数据概览"""
    from app.services.stock.stock_index_pe_lg_service import StockIndexPeLgService
    service = StockIndexPeLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_index_pe_lg/refresh")
async def refresh_stock_index_pe_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新指数市盈率数据"""
    from app.services.stock.stock_index_pe_lg_service import StockIndexPeLgService
    service = StockIndexPeLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_index_pe_lg/clear")
async def clear_stock_index_pe_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空指数市盈率数据"""
    from app.services.stock.stock_index_pe_lg_service import StockIndexPeLgService
    service = StockIndexPeLgService(db)
    return await service.clear_data()



# 个股信息查询-雪球 - stock_individual_basic_info_hk_xq
@router.get("/collections/stock_individual_basic_info_hk_xq")
async def get_stock_individual_basic_info_hk_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_basic_info_hk_xq/overview")
async def get_stock_individual_basic_info_hk_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据概览"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_basic_info_hk_xq/refresh")
async def refresh_stock_individual_basic_info_hk_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_basic_info_hk_xq/clear")
async def clear_stock_individual_basic_info_hk_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_hk_xq_service import StockIndividualBasicInfoHkXqService
    service = StockIndividualBasicInfoHkXqService(db)
    return await service.clear_data()



# 个股信息查询-雪球 - stock_individual_basic_info_us_xq
@router.get("/collections/stock_individual_basic_info_us_xq")
async def get_stock_individual_basic_info_us_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_us_xq_service import StockIndividualBasicInfoUsXqService
    service = StockIndividualBasicInfoUsXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_basic_info_us_xq/overview")
async def get_stock_individual_basic_info_us_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据概览"""
    from app.services.stock.stock_individual_basic_info_us_xq_service import StockIndividualBasicInfoUsXqService
    service = StockIndividualBasicInfoUsXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_basic_info_us_xq/refresh")
async def refresh_stock_individual_basic_info_us_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_us_xq_service import StockIndividualBasicInfoUsXqService
    service = StockIndividualBasicInfoUsXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_basic_info_us_xq/clear")
async def clear_stock_individual_basic_info_us_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_us_xq_service import StockIndividualBasicInfoUsXqService
    service = StockIndividualBasicInfoUsXqService(db)
    return await service.clear_data()



# 个股信息查询-雪球 - stock_individual_basic_info_xq
@router.get("/collections/stock_individual_basic_info_xq")
async def get_stock_individual_basic_info_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_xq_service import StockIndividualBasicInfoXqService
    service = StockIndividualBasicInfoXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_basic_info_xq/overview")
async def get_stock_individual_basic_info_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-雪球数据概览"""
    from app.services.stock.stock_individual_basic_info_xq_service import StockIndividualBasicInfoXqService
    service = StockIndividualBasicInfoXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_basic_info_xq/refresh")
async def refresh_stock_individual_basic_info_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_xq_service import StockIndividualBasicInfoXqService
    service = StockIndividualBasicInfoXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_basic_info_xq/clear")
async def clear_stock_individual_basic_info_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-雪球数据"""
    from app.services.stock.stock_individual_basic_info_xq_service import StockIndividualBasicInfoXqService
    service = StockIndividualBasicInfoXqService(db)
    return await service.clear_data()



# 个股信息查询-东财 - stock_individual_info_em
@router.get("/collections/stock_individual_info_em")
async def get_stock_individual_info_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_info_em/overview")
async def get_stock_individual_info_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股信息查询-东财数据概览"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_info_em/refresh")
async def refresh_stock_individual_info_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_info_em/clear")
async def clear_stock_individual_info_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股信息查询-东财数据"""
    from app.services.stock.stock_individual_info_em_service import StockIndividualInfoEmService
    service = StockIndividualInfoEmService(db)
    return await service.clear_data()



# 实时行情数据-雪球 - stock_individual_spot_xq
@router.get("/collections/stock_individual_spot_xq")
async def get_stock_individual_spot_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-雪球数据"""
    from app.services.stock.stock_individual_spot_xq_service import StockIndividualSpotXqService
    service = StockIndividualSpotXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_individual_spot_xq/overview")
async def get_stock_individual_spot_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-雪球数据概览"""
    from app.services.stock.stock_individual_spot_xq_service import StockIndividualSpotXqService
    service = StockIndividualSpotXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_individual_spot_xq/refresh")
async def refresh_stock_individual_spot_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-雪球数据"""
    from app.services.stock.stock_individual_spot_xq_service import StockIndividualSpotXqService
    service = StockIndividualSpotXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_individual_spot_xq/clear")
async def clear_stock_individual_spot_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-雪球数据"""
    from app.services.stock.stock_individual_spot_xq_service import StockIndividualSpotXqService
    service = StockIndividualSpotXqService(db)
    return await service.clear_data()



# 行业分类数据-巨潮资讯 - stock_industry_category_cninfo
@router.get("/collections/stock_industry_category_cninfo")
async def get_stock_industry_category_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业分类数据-巨潮资讯数据"""
    from app.services.stock.stock_industry_category_cninfo_service import StockIndustryCategoryCninfoService
    service = StockIndustryCategoryCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_category_cninfo/overview")
async def get_stock_industry_category_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业分类数据-巨潮资讯数据概览"""
    from app.services.stock.stock_industry_category_cninfo_service import StockIndustryCategoryCninfoService
    service = StockIndustryCategoryCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_category_cninfo/refresh")
async def refresh_stock_industry_category_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行业分类数据-巨潮资讯数据"""
    from app.services.stock.stock_industry_category_cninfo_service import StockIndustryCategoryCninfoService
    service = StockIndustryCategoryCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_category_cninfo/clear")
async def clear_stock_industry_category_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行业分类数据-巨潮资讯数据"""
    from app.services.stock.stock_industry_category_cninfo_service import StockIndustryCategoryCninfoService
    service = StockIndustryCategoryCninfoService(db)
    return await service.clear_data()



# 上市公司行业归属的变动情况-巨潮资讯 - stock_industry_change_cninfo
@router.get("/collections/stock_industry_change_cninfo")
async def get_stock_industry_change_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司行业归属的变动情况-巨潮资讯数据"""
    from app.services.stock.stock_industry_change_cninfo_service import StockIndustryChangeCninfoService
    service = StockIndustryChangeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_change_cninfo/overview")
async def get_stock_industry_change_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市公司行业归属的变动情况-巨潮资讯数据概览"""
    from app.services.stock.stock_industry_change_cninfo_service import StockIndustryChangeCninfoService
    service = StockIndustryChangeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_change_cninfo/refresh")
async def refresh_stock_industry_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市公司行业归属的变动情况-巨潮资讯数据"""
    from app.services.stock.stock_industry_change_cninfo_service import StockIndustryChangeCninfoService
    service = StockIndustryChangeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_change_cninfo/clear")
async def clear_stock_industry_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市公司行业归属的变动情况-巨潮资讯数据"""
    from app.services.stock.stock_industry_change_cninfo_service import StockIndustryChangeCninfoService
    service = StockIndustryChangeCninfoService(db)
    return await service.clear_data()



# 申万个股行业分类变动历史 - stock_industry_clf_hist_sw
@router.get("/collections/stock_industry_clf_hist_sw")
async def get_stock_industry_clf_hist_sw(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_clf_hist_sw/overview")
async def get_stock_industry_clf_hist_sw_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取申万个股行业分类变动历史数据概览"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_clf_hist_sw/refresh")
async def refresh_stock_industry_clf_hist_sw(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_clf_hist_sw/clear")
async def clear_stock_industry_clf_hist_sw(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空申万个股行业分类变动历史数据"""
    from app.services.stock.stock_industry_clf_hist_sw_service import StockIndustryClfHistSwService
    service = StockIndustryClfHistSwService(db)
    return await service.clear_data()



# 行业市盈率 - stock_industry_pe_ratio_cninfo
@router.get("/collections/stock_industry_pe_ratio_cninfo")
async def get_stock_industry_pe_ratio_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_industry_pe_ratio_cninfo/overview")
async def get_stock_industry_pe_ratio_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业市盈率数据概览"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_industry_pe_ratio_cninfo/refresh")
async def refresh_stock_industry_pe_ratio_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_industry_pe_ratio_cninfo/clear")
async def clear_stock_industry_pe_ratio_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行业市盈率数据"""
    from app.services.stock.stock_industry_pe_ratio_cninfo_service import StockIndustryPeRatioCninfoService
    service = StockIndustryPeRatioCninfoService(db)
    return await service.clear_data()



# 股票列表-A股 - stock_info_a_code_name
@router.get("/collections/stock_info_a_code_name")
async def get_stock_info_a_code_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_a_code_name/overview")
async def get_stock_info_a_code_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-A股数据概览"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_a_code_name/refresh")
async def refresh_stock_info_a_code_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_a_code_name/clear")
async def clear_stock_info_a_code_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-A股数据"""
    from app.services.stock.stock_info_a_code_name_service import StockInfoACodeNameService
    service = StockInfoACodeNameService(db)
    return await service.clear_data()



# 股票列表-北证 - stock_info_bj_name_code
@router.get("/collections/stock_info_bj_name_code")
async def get_stock_info_bj_name_code(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_bj_name_code/overview")
async def get_stock_info_bj_name_code_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-北证数据概览"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_bj_name_code/refresh")
async def refresh_stock_info_bj_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_bj_name_code/clear")
async def clear_stock_info_bj_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-北证数据"""
    from app.services.stock.stock_info_bj_name_code_service import StockInfoBjNameCodeService
    service = StockInfoBjNameCodeService(db)
    return await service.clear_data()



# 股票更名 - stock_info_change_name
@router.get("/collections/stock_info_change_name")
async def get_stock_info_change_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票更名数据"""
    from app.services.stock.stock_info_change_name_service import StockInfoChangeNameService
    service = StockInfoChangeNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_change_name/overview")
async def get_stock_info_change_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票更名数据概览"""
    from app.services.stock.stock_info_change_name_service import StockInfoChangeNameService
    service = StockInfoChangeNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_change_name/refresh")
async def refresh_stock_info_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票更名数据"""
    from app.services.stock.stock_info_change_name_service import StockInfoChangeNameService
    service = StockInfoChangeNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_change_name/clear")
async def clear_stock_info_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票更名数据"""
    from app.services.stock.stock_info_change_name_service import StockInfoChangeNameService
    service = StockInfoChangeNameService(db)
    return await service.clear_data()



# 暂停-终止上市-上证 - stock_info_sh_delist
@router.get("/collections/stock_info_sh_delist")
async def get_stock_info_sh_delist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sh_delist/overview")
async def get_stock_info_sh_delist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取暂停-终止上市-上证数据概览"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sh_delist/refresh")
async def refresh_stock_info_sh_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sh_delist/clear")
async def clear_stock_info_sh_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空暂停-终止上市-上证数据"""
    from app.services.stock.stock_info_sh_delist_service import StockInfoShDelistService
    service = StockInfoShDelistService(db)
    return await service.clear_data()



# 股票列表-上证 - stock_info_sh_name_code
@router.get("/collections/stock_info_sh_name_code")
async def get_stock_info_sh_name_code(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-上证数据"""
    from app.services.stock.stock_info_sh_name_code_service import StockInfoShNameCodeService
    service = StockInfoShNameCodeService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sh_name_code/overview")
async def get_stock_info_sh_name_code_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-上证数据概览"""
    from app.services.stock.stock_info_sh_name_code_service import StockInfoShNameCodeService
    service = StockInfoShNameCodeService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sh_name_code/refresh")
async def refresh_stock_info_sh_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-上证数据"""
    from app.services.stock.stock_info_sh_name_code_service import StockInfoShNameCodeService
    service = StockInfoShNameCodeService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sh_name_code/clear")
async def clear_stock_info_sh_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-上证数据"""
    from app.services.stock.stock_info_sh_name_code_service import StockInfoShNameCodeService
    service = StockInfoShNameCodeService(db)
    return await service.clear_data()



# 名称变更-深证 - stock_info_sz_change_name
@router.get("/collections/stock_info_sz_change_name")
async def get_stock_info_sz_change_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sz_change_name/overview")
async def get_stock_info_sz_change_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取名称变更-深证数据概览"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sz_change_name/refresh")
async def refresh_stock_info_sz_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sz_change_name/clear")
async def clear_stock_info_sz_change_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空名称变更-深证数据"""
    from app.services.stock.stock_info_sz_change_name_service import StockInfoSzChangeNameService
    service = StockInfoSzChangeNameService(db)
    return await service.clear_data()



# 终止-暂停上市-深证 - stock_info_sz_delist
@router.get("/collections/stock_info_sz_delist")
async def get_stock_info_sz_delist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sz_delist/overview")
async def get_stock_info_sz_delist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取终止-暂停上市-深证数据概览"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sz_delist/refresh")
async def refresh_stock_info_sz_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sz_delist/clear")
async def clear_stock_info_sz_delist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空终止-暂停上市-深证数据"""
    from app.services.stock.stock_info_sz_delist_service import StockInfoSzDelistService
    service = StockInfoSzDelistService(db)
    return await service.clear_data()



# 股票列表-深证 - stock_info_sz_name_code
@router.get("/collections/stock_info_sz_name_code")
async def get_stock_info_sz_name_code(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-深证数据"""
    from app.services.stock.stock_info_sz_name_code_service import StockInfoSzNameCodeService
    service = StockInfoSzNameCodeService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_info_sz_name_code/overview")
async def get_stock_info_sz_name_code_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票列表-深证数据概览"""
    from app.services.stock.stock_info_sz_name_code_service import StockInfoSzNameCodeService
    service = StockInfoSzNameCodeService(db)
    return await service.get_overview()


@router.post("/collections/stock_info_sz_name_code/refresh")
async def refresh_stock_info_sz_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票列表-深证数据"""
    from app.services.stock.stock_info_sz_name_code_service import StockInfoSzNameCodeService
    service = StockInfoSzNameCodeService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_info_sz_name_code/clear")
async def clear_stock_info_sz_name_code(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票列表-深证数据"""
    from app.services.stock.stock_info_sz_name_code_service import StockInfoSzNameCodeService
    service = StockInfoSzNameCodeService(db)
    return await service.clear_data()



# 内部交易 - stock_inner_trade_xq
@router.get("/collections/stock_inner_trade_xq")
async def get_stock_inner_trade_xq(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_inner_trade_xq/overview")
async def get_stock_inner_trade_xq_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取内部交易数据概览"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.get_overview()


@router.post("/collections/stock_inner_trade_xq/refresh")
async def refresh_stock_inner_trade_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_inner_trade_xq/clear")
async def clear_stock_inner_trade_xq(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空内部交易数据"""
    from app.services.stock.stock_inner_trade_xq_service import StockInnerTradeXqService
    service = StockInnerTradeXqService(db)
    return await service.clear_data()



# 机构持股一览表 - stock_institute_hold
@router.get("/collections/stock_institute_hold")
async def get_stock_institute_hold(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_hold/overview")
async def get_stock_institute_hold_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股一览表数据概览"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_hold/refresh")
async def refresh_stock_institute_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_hold/clear")
async def clear_stock_institute_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构持股一览表数据"""
    from app.services.stock.stock_institute_hold_service import StockInstituteHoldService
    service = StockInstituteHoldService(db)
    return await service.clear_data()



# 机构持股详情 - stock_institute_hold_detail
@router.get("/collections/stock_institute_hold_detail")
async def get_stock_institute_hold_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_hold_detail/overview")
async def get_stock_institute_hold_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构持股详情数据概览"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_hold_detail/refresh")
async def refresh_stock_institute_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_hold_detail/clear")
async def clear_stock_institute_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构持股详情数据"""
    from app.services.stock.stock_institute_hold_detail_service import StockInstituteHoldDetailService
    service = StockInstituteHoldDetailService(db)
    return await service.clear_data()



# 机构推荐池 - stock_institute_recommend
@router.get("/collections/stock_institute_recommend")
async def get_stock_institute_recommend(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_recommend/overview")
async def get_stock_institute_recommend_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构推荐池数据概览"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_recommend/refresh")
async def refresh_stock_institute_recommend(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_recommend/clear")
async def clear_stock_institute_recommend(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构推荐池数据"""
    from app.services.stock.stock_institute_recommend_service import StockInstituteRecommendService
    service = StockInstituteRecommendService(db)
    return await service.clear_data()



# 股票评级记录 - stock_institute_recommend_detail
@router.get("/collections/stock_institute_recommend_detail")
async def get_stock_institute_recommend_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_institute_recommend_detail/overview")
async def get_stock_institute_recommend_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票评级记录数据概览"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_institute_recommend_detail/refresh")
async def refresh_stock_institute_recommend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_institute_recommend_detail/clear")
async def clear_stock_institute_recommend_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票评级记录数据"""
    from app.services.stock.stock_institute_recommend_detail_service import StockInstituteRecommendDetailService
    service = StockInstituteRecommendDetailService(db)
    return await service.clear_data()



# 日内分时数据-东财 - stock_intraday_em
@router.get("/collections/stock_intraday_em")
async def get_stock_intraday_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_intraday_em/overview")
async def get_stock_intraday_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-东财数据概览"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_intraday_em/refresh")
async def refresh_stock_intraday_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_intraday_em/clear")
async def clear_stock_intraday_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空日内分时数据-东财数据"""
    from app.services.stock.stock_intraday_em_service import StockIntradayEmService
    service = StockIntradayEmService(db)
    return await service.clear_data()



# 日内分时数据-新浪 - stock_intraday_sina
@router.get("/collections/stock_intraday_sina")
async def get_stock_intraday_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_intraday_sina/overview")
async def get_stock_intraday_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取日内分时数据-新浪数据概览"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_intraday_sina/refresh")
async def refresh_stock_intraday_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_intraday_sina/clear")
async def clear_stock_intraday_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空日内分时数据-新浪数据"""
    from app.services.stock.stock_intraday_sina_service import StockIntradaySinaService
    service = StockIntradaySinaService(db)
    return await service.clear_data()



# IPO 受益股 - stock_ipo_benefit_ths
@router.get("/collections/stock_ipo_benefit_ths")
async def get_stock_ipo_benefit_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_benefit_ths/overview")
async def get_stock_ipo_benefit_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取IPO 受益股数据概览"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_benefit_ths/refresh")
async def refresh_stock_ipo_benefit_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_benefit_ths/clear")
async def clear_stock_ipo_benefit_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空IPO 受益股数据"""
    from app.services.stock.stock_ipo_benefit_ths_service import StockIpoBenefitThsService
    service = StockIpoBenefitThsService(db)
    return await service.clear_data()



# 首发申报信息 - stock_ipo_declare
@router.get("/collections/stock_ipo_declare")
async def get_stock_ipo_declare(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_declare/overview")
async def get_stock_ipo_declare_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取首发申报信息数据概览"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_declare/refresh")
async def refresh_stock_ipo_declare(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_declare/clear")
async def clear_stock_ipo_declare(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空首发申报信息数据"""
    from app.services.stock.stock_ipo_declare_service import StockIpoDeclareService
    service = StockIpoDeclareService(db)
    return await service.clear_data()



# 上市相关-巨潮资讯 - stock_ipo_summary_cninfo
@router.get("/collections/stock_ipo_summary_cninfo")
async def get_stock_ipo_summary_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_ipo_summary_cninfo/overview")
async def get_stock_ipo_summary_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上市相关-巨潮资讯数据概览"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_ipo_summary_cninfo/refresh")
async def refresh_stock_ipo_summary_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_ipo_summary_cninfo/clear")
async def clear_stock_ipo_summary_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上市相关-巨潮资讯数据"""
    from app.services.stock.stock_ipo_summary_cninfo_service import StockIpoSummaryCninfoService
    service = StockIpoSummaryCninfoService(db)
    return await service.clear_data()



# 互动易-回答 - stock_irm_ans_cninfo
@router.get("/collections/stock_irm_ans_cninfo")
async def get_stock_irm_ans_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_irm_ans_cninfo/overview")
async def get_stock_irm_ans_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-回答数据概览"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_irm_ans_cninfo/refresh")
async def refresh_stock_irm_ans_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_irm_ans_cninfo/clear")
async def clear_stock_irm_ans_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空互动易-回答数据"""
    from app.services.stock.stock_irm_ans_cninfo_service import StockIrmAnsCninfoService
    service = StockIrmAnsCninfoService(db)
    return await service.clear_data()



# 互动易-提问 - stock_irm_cninfo
@router.get("/collections/stock_irm_cninfo")
async def get_stock_irm_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_irm_cninfo/overview")
async def get_stock_irm_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取互动易-提问数据概览"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_irm_cninfo/refresh")
async def refresh_stock_irm_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_irm_cninfo/clear")
async def clear_stock_irm_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空互动易-提问数据"""
    from app.services.stock.stock_irm_cninfo_service import StockIrmCninfoService
    service = StockIrmCninfoService(db)
    return await service.clear_data()



# 科创板 - stock_kc_a_spot_em
@router.get("/collections/stock_kc_a_spot_em")
async def get_stock_kc_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据"""
    from app.services.stock.stock_kc_a_spot_em_service import StockKcASpotEmService
    service = StockKcASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_kc_a_spot_em/overview")
async def get_stock_kc_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据概览"""
    from app.services.stock.stock_kc_a_spot_em_service import StockKcASpotEmService
    service = StockKcASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_kc_a_spot_em/refresh")
async def refresh_stock_kc_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新科创板数据"""
    from app.services.stock.stock_kc_a_spot_em_service import StockKcASpotEmService
    service = StockKcASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_kc_a_spot_em/clear")
async def clear_stock_kc_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空科创板数据"""
    from app.services.stock.stock_kc_a_spot_em_service import StockKcASpotEmService
    service = StockKcASpotEmService(db)
    return await service.clear_data()



# 龙虎榜-营业部排行-资金实力最强 - stock_lh_yyb_capital
@router.get("/collections/stock_lh_yyb_capital")
async def get_stock_lh_yyb_capital(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_capital/overview")
async def get_stock_lh_yyb_capital_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-资金实力最强数据概览"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_capital/refresh")
async def refresh_stock_lh_yyb_capital(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_capital/clear")
async def clear_stock_lh_yyb_capital(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-资金实力最强数据"""
    from app.services.stock.stock_lh_yyb_capital_service import StockLhYybCapitalService
    service = StockLhYybCapitalService(db)
    return await service.clear_data()



# 龙虎榜-营业部排行-抱团操作实力 - stock_lh_yyb_control
@router.get("/collections/stock_lh_yyb_control")
async def get_stock_lh_yyb_control(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_control/overview")
async def get_stock_lh_yyb_control_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-抱团操作实力数据概览"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_control/refresh")
async def refresh_stock_lh_yyb_control(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_control/clear")
async def clear_stock_lh_yyb_control(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-抱团操作实力数据"""
    from app.services.stock.stock_lh_yyb_control_service import StockLhYybControlService
    service = StockLhYybControlService(db)
    return await service.clear_data()



# 龙虎榜-营业部排行-上榜次数最多 - stock_lh_yyb_most
@router.get("/collections/stock_lh_yyb_most")
async def get_stock_lh_yyb_most(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lh_yyb_most/overview")
async def get_stock_lh_yyb_most_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业部排行-上榜次数最多数据概览"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.get_overview()


@router.post("/collections/stock_lh_yyb_most/refresh")
async def refresh_stock_lh_yyb_most(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lh_yyb_most/clear")
async def clear_stock_lh_yyb_most(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业部排行-上榜次数最多数据"""
    from app.services.stock.stock_lh_yyb_most_service import StockLhYybMostService
    service = StockLhYybMostService(db)
    return await service.clear_data()



# 龙虎榜-每日详情 - stock_lhb_detail_daily_sina
@router.get("/collections/stock_lhb_detail_daily_sina")
async def get_stock_lhb_detail_daily_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-每日详情数据"""
    from app.services.stock.stock_lhb_detail_daily_sina_service import StockLhbDetailDailySinaService
    service = StockLhbDetailDailySinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_detail_daily_sina/overview")
async def get_stock_lhb_detail_daily_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-每日详情数据概览"""
    from app.services.stock.stock_lhb_detail_daily_sina_service import StockLhbDetailDailySinaService
    service = StockLhbDetailDailySinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_detail_daily_sina/refresh")
async def refresh_stock_lhb_detail_daily_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-每日详情数据"""
    from app.services.stock.stock_lhb_detail_daily_sina_service import StockLhbDetailDailySinaService
    service = StockLhbDetailDailySinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_detail_daily_sina/clear")
async def clear_stock_lhb_detail_daily_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-每日详情数据"""
    from app.services.stock.stock_lhb_detail_daily_sina_service import StockLhbDetailDailySinaService
    service = StockLhbDetailDailySinaService(db)
    return await service.clear_data()



# 龙虎榜详情 - stock_lhb_detail_em
@router.get("/collections/stock_lhb_detail_em")
async def get_stock_lhb_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜详情数据"""
    from app.services.stock.stock_lhb_detail_em_service import StockLhbDetailEmService
    service = StockLhbDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_detail_em/overview")
async def get_stock_lhb_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜详情数据概览"""
    from app.services.stock.stock_lhb_detail_em_service import StockLhbDetailEmService
    service = StockLhbDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_detail_em/refresh")
async def refresh_stock_lhb_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜详情数据"""
    from app.services.stock.stock_lhb_detail_em_service import StockLhbDetailEmService
    service = StockLhbDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_detail_em/clear")
async def clear_stock_lhb_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜详情数据"""
    from app.services.stock.stock_lhb_detail_em_service import StockLhbDetailEmService
    service = StockLhbDetailEmService(db)
    return await service.clear_data()



# 龙虎榜-个股上榜统计 - stock_lhb_ggtj_sina
@router.get("/collections/stock_lhb_ggtj_sina")
async def get_stock_lhb_ggtj_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-个股上榜统计数据"""
    from app.services.stock.stock_lhb_ggtj_sina_service import StockLhbGgtjSinaService
    service = StockLhbGgtjSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_ggtj_sina/overview")
async def get_stock_lhb_ggtj_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-个股上榜统计数据概览"""
    from app.services.stock.stock_lhb_ggtj_sina_service import StockLhbGgtjSinaService
    service = StockLhbGgtjSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_ggtj_sina/refresh")
async def refresh_stock_lhb_ggtj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-个股上榜统计数据"""
    from app.services.stock.stock_lhb_ggtj_sina_service import StockLhbGgtjSinaService
    service = StockLhbGgtjSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_ggtj_sina/clear")
async def clear_stock_lhb_ggtj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-个股上榜统计数据"""
    from app.services.stock.stock_lhb_ggtj_sina_service import StockLhbGgtjSinaService
    service = StockLhbGgtjSinaService(db)
    return await service.clear_data()



# 每日活跃营业部 - stock_lhb_hyyyb_em
@router.get("/collections/stock_lhb_hyyyb_em")
async def get_stock_lhb_hyyyb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_hyyyb_em/overview")
async def get_stock_lhb_hyyyb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取每日活跃营业部数据概览"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_hyyyb_em/refresh")
async def refresh_stock_lhb_hyyyb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_hyyyb_em/clear")
async def clear_stock_lhb_hyyyb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空每日活跃营业部数据"""
    from app.services.stock.stock_lhb_hyyyb_em_service import StockLhbHyyybEmService
    service = StockLhbHyyybEmService(db)
    return await service.clear_data()



# 机构买卖每日统计 - stock_lhb_jgmmtj_em
@router.get("/collections/stock_lhb_jgmmtj_em")
async def get_stock_lhb_jgmmtj_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgmmtj_em/overview")
async def get_stock_lhb_jgmmtj_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构买卖每日统计数据概览"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgmmtj_em/refresh")
async def refresh_stock_lhb_jgmmtj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgmmtj_em/clear")
async def clear_stock_lhb_jgmmtj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构买卖每日统计数据"""
    from app.services.stock.stock_lhb_jgmmtj_em_service import StockLhbJgmmtjEmService
    service = StockLhbJgmmtjEmService(db)
    return await service.clear_data()



# 龙虎榜-机构席位成交明细 - stock_lhb_jgmx_sina
@router.get("/collections/stock_lhb_jgmx_sina")
async def get_stock_lhb_jgmx_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgmx_sina/overview")
async def get_stock_lhb_jgmx_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位成交明细数据概览"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgmx_sina/refresh")
async def refresh_stock_lhb_jgmx_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgmx_sina/clear")
async def clear_stock_lhb_jgmx_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-机构席位成交明细数据"""
    from app.services.stock.stock_lhb_jgmx_sina_service import StockLhbJgmxSinaService
    service = StockLhbJgmxSinaService(db)
    return await service.clear_data()



# 机构席位追踪 - stock_lhb_jgstatistic_em
@router.get("/collections/stock_lhb_jgstatistic_em")
async def get_stock_lhb_jgstatistic_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgstatistic_em/overview")
async def get_stock_lhb_jgstatistic_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取机构席位追踪数据概览"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgstatistic_em/refresh")
async def refresh_stock_lhb_jgstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgstatistic_em/clear")
async def clear_stock_lhb_jgstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgstatistic_em_service import StockLhbJgstatisticEmService
    service = StockLhbJgstatisticEmService(db)
    return await service.clear_data()



# 龙虎榜-机构席位追踪 - stock_lhb_jgzz_sina
@router.get("/collections/stock_lhb_jgzz_sina")
async def get_stock_lhb_jgzz_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgzz_sina_service import StockLhbJgzzSinaService
    service = StockLhbJgzzSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_jgzz_sina/overview")
async def get_stock_lhb_jgzz_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-机构席位追踪数据概览"""
    from app.services.stock.stock_lhb_jgzz_sina_service import StockLhbJgzzSinaService
    service = StockLhbJgzzSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_jgzz_sina/refresh")
async def refresh_stock_lhb_jgzz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgzz_sina_service import StockLhbJgzzSinaService
    service = StockLhbJgzzSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_jgzz_sina/clear")
async def clear_stock_lhb_jgzz_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-机构席位追踪数据"""
    from app.services.stock.stock_lhb_jgzz_sina_service import StockLhbJgzzSinaService
    service = StockLhbJgzzSinaService(db)
    return await service.clear_data()



# 个股龙虎榜详情 - stock_lhb_stock_detail_em
@router.get("/collections/stock_lhb_stock_detail_em")
async def get_stock_lhb_stock_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_stock_detail_em/overview")
async def get_stock_lhb_stock_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股龙虎榜详情数据概览"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_stock_detail_em/refresh")
async def refresh_stock_lhb_stock_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_stock_detail_em/clear")
async def clear_stock_lhb_stock_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股龙虎榜详情数据"""
    from app.services.stock.stock_lhb_stock_detail_em_service import StockLhbStockDetailEmService
    service = StockLhbStockDetailEmService(db)
    return await service.clear_data()



# 个股上榜统计 - stock_lhb_stock_statistic_em
@router.get("/collections/stock_lhb_stock_statistic_em")
async def get_stock_lhb_stock_statistic_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股上榜统计数据"""
    from app.services.stock.stock_lhb_stock_statistic_em_service import StockLhbStockStatisticEmService
    service = StockLhbStockStatisticEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_stock_statistic_em/overview")
async def get_stock_lhb_stock_statistic_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股上榜统计数据概览"""
    from app.services.stock.stock_lhb_stock_statistic_em_service import StockLhbStockStatisticEmService
    service = StockLhbStockStatisticEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_stock_statistic_em/refresh")
async def refresh_stock_lhb_stock_statistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股上榜统计数据"""
    from app.services.stock.stock_lhb_stock_statistic_em_service import StockLhbStockStatisticEmService
    service = StockLhbStockStatisticEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_stock_statistic_em/clear")
async def clear_stock_lhb_stock_statistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股上榜统计数据"""
    from app.services.stock.stock_lhb_stock_statistic_em_service import StockLhbStockStatisticEmService
    service = StockLhbStockStatisticEmService(db)
    return await service.clear_data()



# 营业部统计 - stock_lhb_traderstatistic_em
@router.get("/collections/stock_lhb_traderstatistic_em")
async def get_stock_lhb_traderstatistic_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_traderstatistic_em/overview")
async def get_stock_lhb_traderstatistic_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部统计数据概览"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_traderstatistic_em/refresh")
async def refresh_stock_lhb_traderstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_traderstatistic_em/clear")
async def clear_stock_lhb_traderstatistic_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部统计数据"""
    from app.services.stock.stock_lhb_traderstatistic_em_service import StockLhbTraderstatisticEmService
    service = StockLhbTraderstatisticEmService(db)
    return await service.clear_data()



# 营业部详情数据-东财 - stock_lhb_yyb_detail_em
@router.get("/collections/stock_lhb_yyb_detail_em")
async def get_stock_lhb_yyb_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部详情数据-东财数据"""
    from app.services.stock.stock_lhb_yyb_detail_em_service import StockLhbYybDetailEmService
    service = StockLhbYybDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_yyb_detail_em/overview")
async def get_stock_lhb_yyb_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部详情数据-东财数据概览"""
    from app.services.stock.stock_lhb_yyb_detail_em_service import StockLhbYybDetailEmService
    service = StockLhbYybDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_yyb_detail_em/refresh")
async def refresh_stock_lhb_yyb_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部详情数据-东财数据"""
    from app.services.stock.stock_lhb_yyb_detail_em_service import StockLhbYybDetailEmService
    service = StockLhbYybDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_yyb_detail_em/clear")
async def clear_stock_lhb_yyb_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部详情数据-东财数据"""
    from app.services.stock.stock_lhb_yyb_detail_em_service import StockLhbYybDetailEmService
    service = StockLhbYybDetailEmService(db)
    return await service.clear_data()



# 营业部排行 - stock_lhb_yybph_em
@router.get("/collections/stock_lhb_yybph_em")
async def get_stock_lhb_yybph_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据"""
    from app.services.stock.stock_lhb_yybph_em_service import StockLhbYybphEmService
    service = StockLhbYybphEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_yybph_em/overview")
async def get_stock_lhb_yybph_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取营业部排行数据概览"""
    from app.services.stock.stock_lhb_yybph_em_service import StockLhbYybphEmService
    service = StockLhbYybphEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_yybph_em/refresh")
async def refresh_stock_lhb_yybph_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新营业部排行数据"""
    from app.services.stock.stock_lhb_yybph_em_service import StockLhbYybphEmService
    service = StockLhbYybphEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_yybph_em/clear")
async def clear_stock_lhb_yybph_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空营业部排行数据"""
    from app.services.stock.stock_lhb_yybph_em_service import StockLhbYybphEmService
    service = StockLhbYybphEmService(db)
    return await service.clear_data()



# 龙虎榜-营业上榜统计 - stock_lhb_yytj_sina
@router.get("/collections/stock_lhb_yytj_sina")
async def get_stock_lhb_yytj_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lhb_yytj_sina/overview")
async def get_stock_lhb_yytj_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取龙虎榜-营业上榜统计数据概览"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_lhb_yytj_sina/refresh")
async def refresh_stock_lhb_yytj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lhb_yytj_sina/clear")
async def clear_stock_lhb_yytj_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空龙虎榜-营业上榜统计数据"""
    from app.services.stock.stock_lhb_yytj_sina_service import StockLhbYytjSinaService
    service = StockLhbYytjSinaService(db)
    return await service.clear_data()



# 利润表 - stock_lrb_em
@router.get("/collections/stock_lrb_em")
async def get_stock_lrb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表数据"""
    from app.services.stock.stock_lrb_em_service import StockLrbEmService
    service = StockLrbEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_lrb_em/overview")
async def get_stock_lrb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表数据概览"""
    from app.services.stock.stock_lrb_em_service import StockLrbEmService
    service = StockLrbEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_lrb_em/refresh")
async def refresh_stock_lrb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新利润表数据"""
    from app.services.stock.stock_lrb_em_service import StockLrbEmService
    service = StockLrbEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_lrb_em/clear")
async def clear_stock_lrb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空利润表数据"""
    from app.services.stock.stock_lrb_em_service import StockLrbEmService
    service = StockLrbEmService(db)
    return await service.clear_data()



# 主要股东 - stock_main_stock_holder
@router.get("/collections/stock_main_stock_holder")
async def get_stock_main_stock_holder(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_main_stock_holder/overview")
async def get_stock_main_stock_holder_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主要股东数据概览"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.get_overview()


@router.post("/collections/stock_main_stock_holder/refresh")
async def refresh_stock_main_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_main_stock_holder/clear")
async def clear_stock_main_stock_holder(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主要股东数据"""
    from app.services.stock.stock_main_stock_holder_service import StockMainStockHolderService
    service = StockMainStockHolderService(db)
    return await service.clear_data()



# 两融账户信息 - stock_margin_account_info
@router.get("/collections/stock_margin_account_info")
async def get_stock_margin_account_info(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_account_info/overview")
async def get_stock_margin_account_info_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两融账户信息数据概览"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_account_info/refresh")
async def refresh_stock_margin_account_info(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_account_info/clear")
async def clear_stock_margin_account_info(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两融账户信息数据"""
    from app.services.stock.stock_margin_account_info_service import StockMarginAccountInfoService
    service = StockMarginAccountInfoService(db)
    return await service.clear_data()



# 融资融券明细 - stock_margin_detail_sse
@router.get("/collections/stock_margin_detail_sse")
async def get_stock_margin_detail_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_detail_sse/overview")
async def get_stock_margin_detail_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据概览"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_detail_sse/refresh")
async def refresh_stock_margin_detail_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_detail_sse/clear")
async def clear_stock_margin_detail_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空融资融券明细数据"""
    from app.services.stock.stock_margin_detail_sse_service import StockMarginDetailSseService
    service = StockMarginDetailSseService(db)
    return await service.clear_data()



# 融资融券明细 - stock_margin_detail_szse
@router.get("/collections/stock_margin_detail_szse")
async def get_stock_margin_detail_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据"""
    from app.services.stock.stock_margin_detail_szse_service import StockMarginDetailSzseService
    service = StockMarginDetailSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_detail_szse/overview")
async def get_stock_margin_detail_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券明细数据概览"""
    from app.services.stock.stock_margin_detail_szse_service import StockMarginDetailSzseService
    service = StockMarginDetailSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_detail_szse/refresh")
async def refresh_stock_margin_detail_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新融资融券明细数据"""
    from app.services.stock.stock_margin_detail_szse_service import StockMarginDetailSzseService
    service = StockMarginDetailSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_detail_szse/clear")
async def clear_stock_margin_detail_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空融资融券明细数据"""
    from app.services.stock.stock_margin_detail_szse_service import StockMarginDetailSzseService
    service = StockMarginDetailSzseService(db)
    return await service.clear_data()



# 标的证券名单及保证金比例查询 - stock_margin_ratio_pa
@router.get("/collections/stock_margin_ratio_pa")
async def get_stock_margin_ratio_pa(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_ratio_pa/overview")
async def get_stock_margin_ratio_pa_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券名单及保证金比例查询数据概览"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_ratio_pa/refresh")
async def refresh_stock_margin_ratio_pa(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_ratio_pa/clear")
async def clear_stock_margin_ratio_pa(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空标的证券名单及保证金比例查询数据"""
    from app.services.stock.stock_margin_ratio_pa_service import StockMarginRatioPaService
    service = StockMarginRatioPaService(db)
    return await service.clear_data()



# 融资融券汇总 - stock_margin_sse
@router.get("/collections/stock_margin_sse")
async def get_stock_margin_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券汇总数据"""
    from app.services.stock.stock_margin_sse_service import StockMarginSseService
    service = StockMarginSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_sse/overview")
async def get_stock_margin_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券汇总数据概览"""
    from app.services.stock.stock_margin_sse_service import StockMarginSseService
    service = StockMarginSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_sse/refresh")
async def refresh_stock_margin_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新融资融券汇总数据"""
    from app.services.stock.stock_margin_sse_service import StockMarginSseService
    service = StockMarginSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_sse/clear")
async def clear_stock_margin_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空融资融券汇总数据"""
    from app.services.stock.stock_margin_sse_service import StockMarginSseService
    service = StockMarginSseService(db)
    return await service.clear_data()



# 融资融券汇总 - stock_margin_szse
@router.get("/collections/stock_margin_szse")
async def get_stock_margin_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券汇总数据"""
    from app.services.stock.stock_margin_szse_service import StockMarginSzseService
    service = StockMarginSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_szse/overview")
async def get_stock_margin_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取融资融券汇总数据概览"""
    from app.services.stock.stock_margin_szse_service import StockMarginSzseService
    service = StockMarginSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_szse/refresh")
async def refresh_stock_margin_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新融资融券汇总数据"""
    from app.services.stock.stock_margin_szse_service import StockMarginSzseService
    service = StockMarginSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_szse/clear")
async def clear_stock_margin_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空融资融券汇总数据"""
    from app.services.stock.stock_margin_szse_service import StockMarginSzseService
    service = StockMarginSzseService(db)
    return await service.clear_data()



# 标的证券信息 - stock_margin_underlying_info_szse
@router.get("/collections/stock_margin_underlying_info_szse")
async def get_stock_margin_underlying_info_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_margin_underlying_info_szse/overview")
async def get_stock_margin_underlying_info_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取标的证券信息数据概览"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_margin_underlying_info_szse/refresh")
async def refresh_stock_margin_underlying_info_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_margin_underlying_info_szse/clear")
async def clear_stock_margin_underlying_info_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空标的证券信息数据"""
    from app.services.stock.stock_margin_underlying_info_szse_service import StockMarginUnderlyingInfoSzseService
    service = StockMarginUnderlyingInfoSzseService(db)
    return await service.clear_data()



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



# 主板市净率 - stock_market_pb_lg
@router.get("/collections/stock_market_pb_lg")
async def get_stock_market_pb_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_market_pb_lg/overview")
async def get_stock_market_pb_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市净率数据概览"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_market_pb_lg/refresh")
async def refresh_stock_market_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_market_pb_lg/clear")
async def clear_stock_market_pb_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主板市净率数据"""
    from app.services.stock.stock_market_pb_lg_service import StockMarketPbLgService
    service = StockMarketPbLgService(db)
    return await service.clear_data()



# 主板市盈率 - stock_market_pe_lg
@router.get("/collections/stock_market_pe_lg")
async def get_stock_market_pe_lg(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市盈率数据"""
    from app.services.stock.stock_market_pe_lg_service import StockMarketPeLgService
    service = StockMarketPeLgService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_market_pe_lg/overview")
async def get_stock_market_pe_lg_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主板市盈率数据概览"""
    from app.services.stock.stock_market_pe_lg_service import StockMarketPeLgService
    service = StockMarketPeLgService(db)
    return await service.get_overview()


@router.post("/collections/stock_market_pe_lg/refresh")
async def refresh_stock_market_pe_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主板市盈率数据"""
    from app.services.stock.stock_market_pe_lg_service import StockMarketPeLgService
    service = StockMarketPeLgService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_market_pe_lg/clear")
async def clear_stock_market_pe_lg(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主板市盈率数据"""
    from app.services.stock.stock_market_pe_lg_service import StockMarketPeLgService
    service = StockMarketPeLgService(db)
    return await service.clear_data()



# 新股 - stock_new_a_spot_em
@router.get("/collections/stock_new_a_spot_em")
async def get_stock_new_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股数据"""
    from app.services.stock.stock_new_a_spot_em_service import StockNewASpotEmService
    service = StockNewASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_new_a_spot_em/overview")
async def get_stock_new_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股数据概览"""
    from app.services.stock.stock_new_a_spot_em_service import StockNewASpotEmService
    service = StockNewASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_new_a_spot_em/refresh")
async def refresh_stock_new_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股数据"""
    from app.services.stock.stock_new_a_spot_em_service import StockNewASpotEmService
    service = StockNewASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_new_a_spot_em/clear")
async def clear_stock_new_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股数据"""
    from app.services.stock.stock_new_a_spot_em_service import StockNewASpotEmService
    service = StockNewASpotEmService(db)
    return await service.clear_data()



# 新股过会 - stock_new_gh_cninfo
@router.get("/collections/stock_new_gh_cninfo")
async def get_stock_new_gh_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_new_gh_cninfo/overview")
async def get_stock_new_gh_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股过会数据概览"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_new_gh_cninfo/refresh")
async def refresh_stock_new_gh_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_new_gh_cninfo/clear")
async def clear_stock_new_gh_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股过会数据"""
    from app.services.stock.stock_new_gh_cninfo_service import StockNewGhCninfoService
    service = StockNewGhCninfoService(db)
    return await service.clear_data()



# 新股发行 - stock_new_ipo_cninfo
@router.get("/collections/stock_new_ipo_cninfo")
async def get_stock_new_ipo_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_new_ipo_cninfo/overview")
async def get_stock_new_ipo_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股发行数据概览"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_new_ipo_cninfo/refresh")
async def refresh_stock_new_ipo_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_new_ipo_cninfo/clear")
async def clear_stock_new_ipo_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股发行数据"""
    from app.services.stock.stock_new_ipo_cninfo_service import StockNewIpoCninfoService
    service = StockNewIpoCninfoService(db)
    return await service.clear_data()



# 财经内容精选 - stock_news_main_cx
@router.get("/collections/stock_news_main_cx")
async def get_stock_news_main_cx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_news_main_cx/overview")
async def get_stock_news_main_cx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取财经内容精选数据概览"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.get_overview()


@router.post("/collections/stock_news_main_cx/refresh")
async def refresh_stock_news_main_cx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_news_main_cx/clear")
async def clear_stock_news_main_cx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空财经内容精选数据"""
    from app.services.stock.stock_news_main_cx_service import StockNewsMainCxService
    service = StockNewsMainCxService(db)
    return await service.clear_data()



# 配股 - stock_pg_em
@router.get("/collections/stock_pg_em")
async def get_stock_pg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_pg_em/overview")
async def get_stock_pg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取配股数据概览"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_pg_em/refresh")
async def refresh_stock_pg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_pg_em/clear")
async def clear_stock_pg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空配股数据"""
    from app.services.stock.stock_pg_em_service import StockPgEmService
    service = StockPgEmService(db)
    return await service.clear_data()



# 美港目标价 - stock_price_js
@router.get("/collections/stock_price_js")
async def get_stock_price_js(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_price_js/overview")
async def get_stock_price_js_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取美港目标价数据概览"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.get_overview()


@router.post("/collections/stock_price_js/refresh")
async def refresh_stock_price_js(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_price_js/clear")
async def clear_stock_price_js(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空美港目标价数据"""
    from app.services.stock.stock_price_js_service import StockPriceJsService
    service = StockPriceJsService(db)
    return await service.clear_data()



# 公司概况-巨潮资讯 - stock_profile_cninfo
@router.get("/collections/stock_profile_cninfo")
async def get_stock_profile_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profile_cninfo/overview")
async def get_stock_profile_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司概况-巨潮资讯数据概览"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_profile_cninfo/refresh")
async def refresh_stock_profile_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profile_cninfo/clear")
async def clear_stock_profile_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司概况-巨潮资讯数据"""
    from app.services.stock.stock_profile_cninfo_service import StockProfileCninfoService
    service = StockProfileCninfoService(db)
    return await service.clear_data()



# 盈利预测-东方财富 - stock_profit_forecast_em
@router.get("/collections/stock_profit_forecast_em")
async def get_stock_profit_forecast_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_forecast_em/overview")
async def get_stock_profit_forecast_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-东方财富数据概览"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_forecast_em/refresh")
async def refresh_stock_profit_forecast_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_forecast_em/clear")
async def clear_stock_profit_forecast_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盈利预测-东方财富数据"""
    from app.services.stock.stock_profit_forecast_em_service import StockProfitForecastEmService
    service = StockProfitForecastEmService(db)
    return await service.clear_data()



# 盈利预测-同花顺 - stock_profit_forecast_ths
@router.get("/collections/stock_profit_forecast_ths")
async def get_stock_profit_forecast_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_forecast_ths/overview")
async def get_stock_profit_forecast_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盈利预测-同花顺数据概览"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_forecast_ths/refresh")
async def refresh_stock_profit_forecast_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_forecast_ths/clear")
async def clear_stock_profit_forecast_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盈利预测-同花顺数据"""
    from app.services.stock.stock_profit_forecast_ths_service import StockProfitForecastThsService
    service = StockProfitForecastThsService(db)
    return await service.clear_data()



# 利润表-按报告期 - stock_profit_sheet_by_report_em
@router.get("/collections/stock_profit_sheet_by_report_em")
async def get_stock_profit_sheet_by_report_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表-按报告期数据"""
    from app.services.stock.stock_profit_sheet_by_report_em_service import StockProfitSheetByReportEmService
    service = StockProfitSheetByReportEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_sheet_by_report_em/overview")
async def get_stock_profit_sheet_by_report_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表-按报告期数据概览"""
    from app.services.stock.stock_profit_sheet_by_report_em_service import StockProfitSheetByReportEmService
    service = StockProfitSheetByReportEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_sheet_by_report_em/refresh")
async def refresh_stock_profit_sheet_by_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新利润表-按报告期数据"""
    from app.services.stock.stock_profit_sheet_by_report_em_service import StockProfitSheetByReportEmService
    service = StockProfitSheetByReportEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_sheet_by_report_em/clear")
async def clear_stock_profit_sheet_by_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空利润表-按报告期数据"""
    from app.services.stock.stock_profit_sheet_by_report_em_service import StockProfitSheetByReportEmService
    service = StockProfitSheetByReportEmService(db)
    return await service.clear_data()



# 利润表-按年度 - stock_profit_sheet_by_yearly_em
@router.get("/collections/stock_profit_sheet_by_yearly_em")
async def get_stock_profit_sheet_by_yearly_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表-按年度数据"""
    from app.services.stock.stock_profit_sheet_by_yearly_em_service import StockProfitSheetByYearlyEmService
    service = StockProfitSheetByYearlyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_profit_sheet_by_yearly_em/overview")
async def get_stock_profit_sheet_by_yearly_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取利润表-按年度数据概览"""
    from app.services.stock.stock_profit_sheet_by_yearly_em_service import StockProfitSheetByYearlyEmService
    service = StockProfitSheetByYearlyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_profit_sheet_by_yearly_em/refresh")
async def refresh_stock_profit_sheet_by_yearly_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新利润表-按年度数据"""
    from app.services.stock.stock_profit_sheet_by_yearly_em_service import StockProfitSheetByYearlyEmService
    service = StockProfitSheetByYearlyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_profit_sheet_by_yearly_em/clear")
async def clear_stock_profit_sheet_by_yearly_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空利润表-按年度数据"""
    from app.services.stock.stock_profit_sheet_by_yearly_em_service import StockProfitSheetByYearlyEmService
    service = StockProfitSheetByYearlyEmService(db)
    return await service.clear_data()



# 增发 - stock_qbzf_em
@router.get("/collections/stock_qbzf_em")
async def get_stock_qbzf_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_qbzf_em/overview")
async def get_stock_qbzf_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取增发数据概览"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_qbzf_em/refresh")
async def refresh_stock_qbzf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_qbzf_em/clear")
async def clear_stock_qbzf_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空增发数据"""
    from app.services.stock.stock_qbzf_em_service import StockQbzfEmService
    service = StockQbzfEmService(db)
    return await service.clear_data()



# 券商业绩月报 - stock_qsjy_em
@router.get("/collections/stock_qsjy_em")
async def get_stock_qsjy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_qsjy_em/overview")
async def get_stock_qsjy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取券商业绩月报数据概览"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_qsjy_em/refresh")
async def refresh_stock_qsjy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_qsjy_em/clear")
async def clear_stock_qsjy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空券商业绩月报数据"""
    from app.services.stock.stock_qsjy_em_service import StockQsjyEmService
    service = StockQsjyEmService(db)
    return await service.clear_data()



# 持续放量 - stock_rank_cxfl_ths
@router.get("/collections/stock_rank_cxfl_ths")
async def get_stock_rank_cxfl_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_cxfl_ths/overview")
async def get_stock_rank_cxfl_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续放量数据概览"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_cxfl_ths/refresh")
async def refresh_stock_rank_cxfl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_cxfl_ths/clear")
async def clear_stock_rank_cxfl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空持续放量数据"""
    from app.services.stock.stock_rank_cxfl_ths_service import StockRankCxflThsService
    service = StockRankCxflThsService(db)
    return await service.clear_data()



# 持续缩量 - stock_rank_cxsl_ths
@router.get("/collections/stock_rank_cxsl_ths")
async def get_stock_rank_cxsl_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_cxsl_ths/overview")
async def get_stock_rank_cxsl_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取持续缩量数据概览"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_cxsl_ths/refresh")
async def refresh_stock_rank_cxsl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_cxsl_ths/clear")
async def clear_stock_rank_cxsl_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空持续缩量数据"""
    from app.services.stock.stock_rank_cxsl_ths_service import StockRankCxslThsService
    service = StockRankCxslThsService(db)
    return await service.clear_data()



# 投资评级 - stock_rank_forecast_cninfo
@router.get("/collections/stock_rank_forecast_cninfo")
async def get_stock_rank_forecast_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_forecast_cninfo/overview")
async def get_stock_rank_forecast_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取投资评级数据概览"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_forecast_cninfo/refresh")
async def refresh_stock_rank_forecast_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_forecast_cninfo/clear")
async def clear_stock_rank_forecast_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空投资评级数据"""
    from app.services.stock.stock_rank_forecast_cninfo_service import StockRankForecastCninfoService
    service = StockRankForecastCninfoService(db)
    return await service.clear_data()



# 量价齐跌 - stock_rank_ljqd_ths
@router.get("/collections/stock_rank_ljqd_ths")
async def get_stock_rank_ljqd_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐跌数据"""
    from app.services.stock.stock_rank_ljqd_ths_service import StockRankLjqdThsService
    service = StockRankLjqdThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_ljqd_ths/overview")
async def get_stock_rank_ljqd_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐跌数据概览"""
    from app.services.stock.stock_rank_ljqd_ths_service import StockRankLjqdThsService
    service = StockRankLjqdThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_ljqd_ths/refresh")
async def refresh_stock_rank_ljqd_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新量价齐跌数据"""
    from app.services.stock.stock_rank_ljqd_ths_service import StockRankLjqdThsService
    service = StockRankLjqdThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_ljqd_ths/clear")
async def clear_stock_rank_ljqd_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空量价齐跌数据"""
    from app.services.stock.stock_rank_ljqd_ths_service import StockRankLjqdThsService
    service = StockRankLjqdThsService(db)
    return await service.clear_data()



# 量价齐升 - stock_rank_ljqs_ths
@router.get("/collections/stock_rank_ljqs_ths")
async def get_stock_rank_ljqs_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_ljqs_ths/overview")
async def get_stock_rank_ljqs_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取量价齐升数据概览"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_ljqs_ths/refresh")
async def refresh_stock_rank_ljqs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_ljqs_ths/clear")
async def clear_stock_rank_ljqs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空量价齐升数据"""
    from app.services.stock.stock_rank_ljqs_ths_service import StockRankLjqsThsService
    service = StockRankLjqsThsService(db)
    return await service.clear_data()



# 向上突破 - stock_rank_xstp_ths
@router.get("/collections/stock_rank_xstp_ths")
async def get_stock_rank_xstp_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_xstp_ths/overview")
async def get_stock_rank_xstp_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向上突破数据概览"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_xstp_ths/refresh")
async def refresh_stock_rank_xstp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_xstp_ths/clear")
async def clear_stock_rank_xstp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空向上突破数据"""
    from app.services.stock.stock_rank_xstp_ths_service import StockRankXstpThsService
    service = StockRankXstpThsService(db)
    return await service.clear_data()



# 向下突破 - stock_rank_xxtp_ths
@router.get("/collections/stock_rank_xxtp_ths")
async def get_stock_rank_xxtp_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向下突破数据"""
    from app.services.stock.stock_rank_xxtp_ths_service import StockRankXxtpThsService
    service = StockRankXxtpThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_xxtp_ths/overview")
async def get_stock_rank_xxtp_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取向下突破数据概览"""
    from app.services.stock.stock_rank_xxtp_ths_service import StockRankXxtpThsService
    service = StockRankXxtpThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_xxtp_ths/refresh")
async def refresh_stock_rank_xxtp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新向下突破数据"""
    from app.services.stock.stock_rank_xxtp_ths_service import StockRankXxtpThsService
    service = StockRankXxtpThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_xxtp_ths/clear")
async def clear_stock_rank_xxtp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空向下突破数据"""
    from app.services.stock.stock_rank_xxtp_ths_service import StockRankXxtpThsService
    service = StockRankXxtpThsService(db)
    return await service.clear_data()



# 险资举牌 - stock_rank_xzjp_ths
@router.get("/collections/stock_rank_xzjp_ths")
async def get_stock_rank_xzjp_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_rank_xzjp_ths/overview")
async def get_stock_rank_xzjp_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取险资举牌数据概览"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_rank_xzjp_ths/refresh")
async def refresh_stock_rank_xzjp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_rank_xzjp_ths/clear")
async def clear_stock_rank_xzjp_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空险资举牌数据"""
    from app.services.stock.stock_rank_xzjp_ths_service import StockRankXzjpThsService
    service = StockRankXzjpThsService(db)
    return await service.clear_data()



# 北交所 - stock_register_bj
@router.get("/collections/stock_register_bj")
async def get_stock_register_bj(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_bj/overview")
async def get_stock_register_bj_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取北交所数据概览"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_bj/refresh")
async def refresh_stock_register_bj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_bj/clear")
async def clear_stock_register_bj(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空北交所数据"""
    from app.services.stock.stock_register_bj_service import StockRegisterBjService
    service = StockRegisterBjService(db)
    return await service.clear_data()



# 创业板 - stock_register_cyb
@router.get("/collections/stock_register_cyb")
async def get_stock_register_cyb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_cyb/overview")
async def get_stock_register_cyb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取创业板数据概览"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_cyb/refresh")
async def refresh_stock_register_cyb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_cyb/clear")
async def clear_stock_register_cyb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空创业板数据"""
    from app.services.stock.stock_register_cyb_service import StockRegisterCybService
    service = StockRegisterCybService(db)
    return await service.clear_data()



# 达标企业 - stock_register_db
@router.get("/collections/stock_register_db")
async def get_stock_register_db(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_db/overview")
async def get_stock_register_db_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取达标企业数据概览"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_db/refresh")
async def refresh_stock_register_db(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_db/clear")
async def clear_stock_register_db(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空达标企业数据"""
    from app.services.stock.stock_register_db_service import StockRegisterDbService
    service = StockRegisterDbService(db)
    return await service.clear_data()



# 科创板 - stock_register_kcb
@router.get("/collections/stock_register_kcb")
async def get_stock_register_kcb(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_kcb/overview")
async def get_stock_register_kcb_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板数据概览"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_kcb/refresh")
async def refresh_stock_register_kcb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_kcb/clear")
async def clear_stock_register_kcb(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空科创板数据"""
    from app.services.stock.stock_register_kcb_service import StockRegisterKcbService
    service = StockRegisterKcbService(db)
    return await service.clear_data()



# 上海主板 - stock_register_sh
@router.get("/collections/stock_register_sh")
async def get_stock_register_sh(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_sh/overview")
async def get_stock_register_sh_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海主板数据概览"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_sh/refresh")
async def refresh_stock_register_sh(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_sh/clear")
async def clear_stock_register_sh(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海主板数据"""
    from app.services.stock.stock_register_sh_service import StockRegisterShService
    service = StockRegisterShService(db)
    return await service.clear_data()



# 深圳主板 - stock_register_sz
@router.get("/collections/stock_register_sz")
async def get_stock_register_sz(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_register_sz/overview")
async def get_stock_register_sz_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深圳主板数据概览"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.get_overview()


@router.post("/collections/stock_register_sz/refresh")
async def refresh_stock_register_sz(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_register_sz/clear")
async def clear_stock_register_sz(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空深圳主板数据"""
    from app.services.stock.stock_register_sz_service import StockRegisterSzService
    service = StockRegisterSzService(db)
    return await service.clear_data()



# 预约披露时间-巨潮资讯 - stock_report_disclosure
@router.get("/collections/stock_report_disclosure")
async def get_stock_report_disclosure(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_disclosure/overview")
async def get_stock_report_disclosure_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取预约披露时间-巨潮资讯数据概览"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_disclosure/refresh")
async def refresh_stock_report_disclosure(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_disclosure/clear")
async def clear_stock_report_disclosure(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空预约披露时间-巨潮资讯数据"""
    from app.services.stock.stock_report_disclosure_service import StockReportDisclosureService
    service = StockReportDisclosureService(db)
    return await service.clear_data()



# 基金持股 - stock_report_fund_hold
@router.get("/collections/stock_report_fund_hold")
async def get_stock_report_fund_hold(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_fund_hold/overview")
async def get_stock_report_fund_hold_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股数据概览"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_fund_hold/refresh")
async def refresh_stock_report_fund_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_fund_hold/clear")
async def clear_stock_report_fund_hold(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股数据"""
    from app.services.stock.stock_report_fund_hold_service import StockReportFundHoldService
    service = StockReportFundHoldService(db)
    return await service.clear_data()



# 基金持股明细 - stock_report_fund_hold_detail
@router.get("/collections/stock_report_fund_hold_detail")
async def get_stock_report_fund_hold_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_report_fund_hold_detail/overview")
async def get_stock_report_fund_hold_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取基金持股明细数据概览"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_report_fund_hold_detail/refresh")
async def refresh_stock_report_fund_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_report_fund_hold_detail/clear")
async def clear_stock_report_fund_hold_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空基金持股明细数据"""
    from app.services.stock.stock_report_fund_hold_detail_service import StockReportFundHoldDetailService
    service = StockReportFundHoldDetailService(db)
    return await service.clear_data()



# 股票回购数据 - stock_repurchase_em
@router.get("/collections/stock_repurchase_em")
async def get_stock_repurchase_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_repurchase_em/overview")
async def get_stock_repurchase_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票回购数据数据概览"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_repurchase_em/refresh")
async def refresh_stock_repurchase_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_repurchase_em/clear")
async def clear_stock_repurchase_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票回购数据数据"""
    from app.services.stock.stock_repurchase_em_service import StockRepurchaseEmService
    service = StockRepurchaseEmService(db)
    return await service.clear_data()



# 限售股解禁详情 - stock_restricted_release_detail_em
@router.get("/collections/stock_restricted_release_detail_em")
async def get_stock_restricted_release_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_detail_em/overview")
async def get_stock_restricted_release_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁详情数据概览"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_detail_em/refresh")
async def refresh_stock_restricted_release_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_detail_em/clear")
async def clear_stock_restricted_release_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空限售股解禁详情数据"""
    from app.services.stock.stock_restricted_release_detail_em_service import StockRestrictedReleaseDetailEmService
    service = StockRestrictedReleaseDetailEmService(db)
    return await service.clear_data()



# 个股限售解禁-新浪 - stock_restricted_release_queue_sina
@router.get("/collections/stock_restricted_release_queue_sina")
async def get_stock_restricted_release_queue_sina(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_queue_sina/overview")
async def get_stock_restricted_release_queue_sina_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股限售解禁-新浪数据概览"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_queue_sina/refresh")
async def refresh_stock_restricted_release_queue_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_queue_sina/clear")
async def clear_stock_restricted_release_queue_sina(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股限售解禁-新浪数据"""
    from app.services.stock.stock_restricted_release_queue_sina_service import StockRestrictedReleaseQueueSinaService
    service = StockRestrictedReleaseQueueSinaService(db)
    return await service.clear_data()



# 解禁股东 - stock_restricted_release_stockholder_em
@router.get("/collections/stock_restricted_release_stockholder_em")
async def get_stock_restricted_release_stockholder_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_stockholder_em/overview")
async def get_stock_restricted_release_stockholder_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取解禁股东数据概览"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_stockholder_em/refresh")
async def refresh_stock_restricted_release_stockholder_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_stockholder_em/clear")
async def clear_stock_restricted_release_stockholder_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空解禁股东数据"""
    from app.services.stock.stock_restricted_release_stockholder_em_service import StockRestrictedReleaseStockholderEmService
    service = StockRestrictedReleaseStockholderEmService(db)
    return await service.clear_data()



# 限售股解禁 - stock_restricted_release_summary_em
@router.get("/collections/stock_restricted_release_summary_em")
async def get_stock_restricted_release_summary_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁数据"""
    from app.services.stock.stock_restricted_release_summary_em_service import StockRestrictedReleaseSummaryEmService
    service = StockRestrictedReleaseSummaryEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_restricted_release_summary_em/overview")
async def get_stock_restricted_release_summary_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取限售股解禁数据概览"""
    from app.services.stock.stock_restricted_release_summary_em_service import StockRestrictedReleaseSummaryEmService
    service = StockRestrictedReleaseSummaryEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_restricted_release_summary_em/refresh")
async def refresh_stock_restricted_release_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新限售股解禁数据"""
    from app.services.stock.stock_restricted_release_summary_em_service import StockRestrictedReleaseSummaryEmService
    service = StockRestrictedReleaseSummaryEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_restricted_release_summary_em/clear")
async def clear_stock_restricted_release_summary_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空限售股解禁数据"""
    from app.services.stock.stock_restricted_release_summary_em_service import StockRestrictedReleaseSummaryEmService
    service = StockRestrictedReleaseSummaryEmService(db)
    return await service.clear_data()



# 板块详情 - stock_sector_detail
@router.get("/collections/stock_sector_detail")
async def get_stock_sector_detail(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sector_detail/overview")
async def get_stock_sector_detail_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块详情数据概览"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.get_overview()


@router.post("/collections/stock_sector_detail/refresh")
async def refresh_stock_sector_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sector_detail/clear")
async def clear_stock_sector_detail(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块详情数据"""
    from app.services.stock.stock_sector_detail_service import StockSectorDetailService
    service = StockSectorDetailService(db)
    return await service.clear_data()



# 板块行情 - stock_sector_spot
@router.get("/collections/stock_sector_spot")
async def get_stock_sector_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sector_spot/overview")
async def get_stock_sector_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取板块行情数据概览"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_sector_spot/refresh")
async def refresh_stock_sector_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sector_spot/clear")
async def clear_stock_sector_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空板块行情数据"""
    from app.services.stock.stock_sector_spot_service import StockSectorSpotService
    service = StockSectorSpotService(db)
    return await service.clear_data()



# 结算汇率-沪港通 - stock_sgt_settlement_exchange_rate_sse
@router.get("/collections/stock_sgt_settlement_exchange_rate_sse")
async def get_stock_sgt_settlement_exchange_rate_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sgt_settlement_exchange_rate_sse/overview")
async def get_stock_sgt_settlement_exchange_rate_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-沪港通数据概览"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_sgt_settlement_exchange_rate_sse/refresh")
async def refresh_stock_sgt_settlement_exchange_rate_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sgt_settlement_exchange_rate_sse/clear")
async def clear_stock_sgt_settlement_exchange_rate_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空结算汇率-沪港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_sse_service import StockSgtSettlementExchangeRateSseService
    service = StockSgtSettlementExchangeRateSseService(db)
    return await service.clear_data()



# 结算汇率-深港通 - stock_sgt_settlement_exchange_rate_szse
@router.get("/collections/stock_sgt_settlement_exchange_rate_szse")
async def get_stock_sgt_settlement_exchange_rate_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sgt_settlement_exchange_rate_szse/overview")
async def get_stock_sgt_settlement_exchange_rate_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取结算汇率-深港通数据概览"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_sgt_settlement_exchange_rate_szse/refresh")
async def refresh_stock_sgt_settlement_exchange_rate_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sgt_settlement_exchange_rate_szse/clear")
async def clear_stock_sgt_settlement_exchange_rate_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空结算汇率-深港通数据"""
    from app.services.stock.stock_sgt_settlement_exchange_rate_szse_service import StockSgtSettlementExchangeRateSzseService
    service = StockSgtSettlementExchangeRateSzseService(db)
    return await service.clear_data()



# 沪 A 股 - stock_sh_a_spot_em
@router.get("/collections/stock_sh_a_spot_em")
async def get_stock_sh_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sh_a_spot_em/overview")
async def get_stock_sh_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪 A 股数据概览"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sh_a_spot_em/refresh")
async def refresh_stock_sh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sh_a_spot_em/clear")
async def clear_stock_sh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪 A 股数据"""
    from app.services.stock.stock_sh_a_spot_em_service import StockShASpotEmService
    service = StockShASpotEmService(db)
    return await service.clear_data()



# 公司股本变动-巨潮资讯 - stock_share_change_cninfo
@router.get("/collections/stock_share_change_cninfo")
async def get_stock_share_change_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_change_cninfo/overview")
async def get_stock_share_change_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司股本变动-巨潮资讯数据概览"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_change_cninfo/refresh")
async def refresh_stock_share_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_change_cninfo/clear")
async def clear_stock_share_change_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司股本变动-巨潮资讯数据"""
    from app.services.stock.stock_share_change_cninfo_service import StockShareChangeCninfoService
    service = StockShareChangeCninfoService(db)
    return await service.clear_data()



# 董监高及相关人员持股变动-北证 - stock_share_hold_change_bse
@router.get("/collections/stock_share_hold_change_bse")
async def get_stock_share_hold_change_bse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-北证数据"""
    from app.services.stock.stock_share_hold_change_bse_service import StockShareHoldChangeBseService
    service = StockShareHoldChangeBseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_hold_change_bse/overview")
async def get_stock_share_hold_change_bse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-北证数据概览"""
    from app.services.stock.stock_share_hold_change_bse_service import StockShareHoldChangeBseService
    service = StockShareHoldChangeBseService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_hold_change_bse/refresh")
async def refresh_stock_share_hold_change_bse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动-北证数据"""
    from app.services.stock.stock_share_hold_change_bse_service import StockShareHoldChangeBseService
    service = StockShareHoldChangeBseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_hold_change_bse/clear")
async def clear_stock_share_hold_change_bse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动-北证数据"""
    from app.services.stock.stock_share_hold_change_bse_service import StockShareHoldChangeBseService
    service = StockShareHoldChangeBseService(db)
    return await service.clear_data()



# 董监高及相关人员持股变动-上证 - stock_share_hold_change_sse
@router.get("/collections/stock_share_hold_change_sse")
async def get_stock_share_hold_change_sse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_hold_change_sse/overview")
async def get_stock_share_hold_change_sse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-上证数据概览"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_hold_change_sse/refresh")
async def refresh_stock_share_hold_change_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_hold_change_sse/clear")
async def clear_stock_share_hold_change_sse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动-上证数据"""
    from app.services.stock.stock_share_hold_change_sse_service import StockShareHoldChangeSseService
    service = StockShareHoldChangeSseService(db)
    return await service.clear_data()



# 董监高及相关人员持股变动-深证 - stock_share_hold_change_szse
@router.get("/collections/stock_share_hold_change_szse")
async def get_stock_share_hold_change_szse(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_share_hold_change_szse/overview")
async def get_stock_share_hold_change_szse_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取董监高及相关人员持股变动-深证数据概览"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.get_overview()


@router.post("/collections/stock_share_hold_change_szse/refresh")
async def refresh_stock_share_hold_change_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_share_hold_change_szse/clear")
async def clear_stock_share_hold_change_szse(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空董监高及相关人员持股变动-深证数据"""
    from app.services.stock.stock_share_hold_change_szse_service import StockShareHoldChangeSzseService
    service = StockShareHoldChangeSzseService(db)
    return await service.clear_data()



# 上证e互动 - stock_sns_sseinfo
@router.get("/collections/stock_sns_sseinfo")
async def get_stock_sns_sseinfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sns_sseinfo/overview")
async def get_stock_sns_sseinfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上证e互动数据概览"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_sns_sseinfo/refresh")
async def refresh_stock_sns_sseinfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sns_sseinfo/clear")
async def clear_stock_sns_sseinfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上证e互动数据"""
    from app.services.stock.stock_sns_sseinfo_service import StockSnsSseinfoService
    service = StockSnsSseinfoService(db)
    return await service.clear_data()



# 上海证券交易所-每日概况 - stock_sse_deal_daily
@router.get("/collections/stock_sse_deal_daily")
async def get_stock_sse_deal_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sse_deal_daily/overview")
async def get_stock_sse_deal_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所-每日概况数据概览"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_sse_deal_daily/refresh")
async def refresh_stock_sse_deal_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sse_deal_daily/clear")
async def clear_stock_sse_deal_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海证券交易所-每日概况数据"""
    from app.services.stock.stock_sse_deal_daily_service import StockSseDealDailyService
    service = StockSseDealDailyService(db)
    return await service.clear_data()



# 上海证券交易所 - stock_sse_summary
@router.get("/collections/stock_sse_summary")
async def get_stock_sse_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sse_summary/overview")
async def get_stock_sse_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取上海证券交易所数据概览"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_sse_summary/refresh")
async def refresh_stock_sse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sse_summary/clear")
async def clear_stock_sse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空上海证券交易所数据"""
    from app.services.stock.stock_sse_summary_service import StockSseSummaryService
    service = StockSseSummaryService(db)
    return await service.clear_data()



# 两网及退市 - stock_staq_net_stop
@router.get("/collections/stock_staq_net_stop")
async def get_stock_staq_net_stop(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_staq_net_stop/overview")
async def get_stock_staq_net_stop_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据概览"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.get_overview()


@router.post("/collections/stock_staq_net_stop/refresh")
async def refresh_stock_staq_net_stop(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_staq_net_stop/clear")
async def clear_stock_staq_net_stop(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两网及退市数据"""
    from app.services.stock.stock_staq_net_stop_service import StockStaqNetStopService
    service = StockStaqNetStopService(db)
    return await service.clear_data()



# 个股商誉明细 - stock_sy_em
@router.get("/collections/stock_sy_em")
async def get_stock_sy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_em/overview")
async def get_stock_sy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉明细数据概览"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_em/refresh")
async def refresh_stock_sy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_em/clear")
async def clear_stock_sy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股商誉明细数据"""
    from app.services.stock.stock_sy_em_service import StockSyEmService
    service = StockSyEmService(db)
    return await service.clear_data()



# 行业商誉 - stock_sy_hy_em
@router.get("/collections/stock_sy_hy_em")
async def get_stock_sy_hy_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_hy_em/overview")
async def get_stock_sy_hy_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取行业商誉数据概览"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_hy_em/refresh")
async def refresh_stock_sy_hy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_hy_em/clear")
async def clear_stock_sy_hy_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空行业商誉数据"""
    from app.services.stock.stock_sy_hy_em_service import StockSyHyEmService
    service = StockSyHyEmService(db)
    return await service.clear_data()



# 个股商誉减值明细 - stock_sy_jz_em
@router.get("/collections/stock_sy_jz_em")
async def get_stock_sy_jz_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉减值明细数据"""
    from app.services.stock.stock_sy_jz_em_service import StockSyJzEmService
    service = StockSyJzEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_jz_em/overview")
async def get_stock_sy_jz_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股商誉减值明细数据概览"""
    from app.services.stock.stock_sy_jz_em_service import StockSyJzEmService
    service = StockSyJzEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_jz_em/refresh")
async def refresh_stock_sy_jz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股商誉减值明细数据"""
    from app.services.stock.stock_sy_jz_em_service import StockSyJzEmService
    service = StockSyJzEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_jz_em/clear")
async def clear_stock_sy_jz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股商誉减值明细数据"""
    from app.services.stock.stock_sy_jz_em_service import StockSyJzEmService
    service = StockSyJzEmService(db)
    return await service.clear_data()



# A股商誉市场概况 - stock_sy_profile_em
@router.get("/collections/stock_sy_profile_em")
async def get_stock_sy_profile_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股商誉市场概况数据"""
    from app.services.stock.stock_sy_profile_em_service import StockSyProfileEmService
    service = StockSyProfileEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_profile_em/overview")
async def get_stock_sy_profile_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股商誉市场概况数据概览"""
    from app.services.stock.stock_sy_profile_em_service import StockSyProfileEmService
    service = StockSyProfileEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_profile_em/refresh")
async def refresh_stock_sy_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股商誉市场概况数据"""
    from app.services.stock.stock_sy_profile_em_service import StockSyProfileEmService
    service = StockSyProfileEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_profile_em/clear")
async def clear_stock_sy_profile_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股商誉市场概况数据"""
    from app.services.stock.stock_sy_profile_em_service import StockSyProfileEmService
    service = StockSyProfileEmService(db)
    return await service.clear_data()



# 商誉减值预期明细 - stock_sy_yq_em
@router.get("/collections/stock_sy_yq_em")
async def get_stock_sy_yq_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sy_yq_em/overview")
async def get_stock_sy_yq_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取商誉减值预期明细数据概览"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sy_yq_em/refresh")
async def refresh_stock_sy_yq_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sy_yq_em/clear")
async def clear_stock_sy_yq_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空商誉减值预期明细数据"""
    from app.services.stock.stock_sy_yq_em_service import StockSyYqEmService
    service = StockSyYqEmService(db)
    return await service.clear_data()



# 深 A 股 - stock_sz_a_spot_em
@router.get("/collections/stock_sz_a_spot_em")
async def get_stock_sz_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深 A 股数据"""
    from app.services.stock.stock_sz_a_spot_em_service import StockSzASpotEmService
    service = StockSzASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_sz_a_spot_em/overview")
async def get_stock_sz_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取深 A 股数据概览"""
    from app.services.stock.stock_sz_a_spot_em_service import StockSzASpotEmService
    service = StockSzASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_sz_a_spot_em/refresh")
async def refresh_stock_sz_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新深 A 股数据"""
    from app.services.stock.stock_sz_a_spot_em_service import StockSzASpotEmService
    service = StockSzASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_sz_a_spot_em/clear")
async def clear_stock_sz_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空深 A 股数据"""
    from app.services.stock.stock_sz_a_spot_em_service import StockSzASpotEmService
    service = StockSzASpotEmService(db)
    return await service.clear_data()



# 地区交易排序 - stock_szse_area_summary
@router.get("/collections/stock_szse_area_summary")
async def get_stock_szse_area_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_area_summary/overview")
async def get_stock_szse_area_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取地区交易排序数据概览"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_area_summary/refresh")
async def refresh_stock_szse_area_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_area_summary/clear")
async def clear_stock_szse_area_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空地区交易排序数据"""
    from app.services.stock.stock_szse_area_summary_service import StockSzseAreaSummaryService
    service = StockSzseAreaSummaryService(db)
    return await service.clear_data()



# 股票行业成交 - stock_szse_sector_summary
@router.get("/collections/stock_szse_sector_summary")
async def get_stock_szse_sector_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_sector_summary/overview")
async def get_stock_szse_sector_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股票行业成交数据概览"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_sector_summary/refresh")
async def refresh_stock_szse_sector_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_sector_summary/clear")
async def clear_stock_szse_sector_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股票行业成交数据"""
    from app.services.stock.stock_szse_sector_summary_service import StockSzseSectorSummaryService
    service = StockSzseSectorSummaryService(db)
    return await service.clear_data()



# 证券类别统计 - stock_szse_summary
@router.get("/collections/stock_szse_summary")
async def get_stock_szse_summary(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_szse_summary/overview")
async def get_stock_szse_summary_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取证券类别统计数据概览"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.get_overview()


@router.post("/collections/stock_szse_summary/refresh")
async def refresh_stock_szse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_szse_summary/clear")
async def clear_stock_szse_summary(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空证券类别统计数据"""
    from app.services.stock.stock_szse_summary_service import StockSzseSummaryService
    service = StockSzseSummaryService(db)
    return await service.clear_data()



# 历史行情数据-新浪 - stock_us_daily
@router.get("/collections/stock_us_daily")
async def get_stock_us_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据"""
    from app.services.stock.stock_us_daily_service import StockUsDailyService
    service = StockUsDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_daily/overview")
async def get_stock_us_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据概览"""
    from app.services.stock.stock_us_daily_service import StockUsDailyService
    service = StockUsDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_daily/refresh")
async def refresh_stock_us_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-新浪数据"""
    from app.services.stock.stock_us_daily_service import StockUsDailyService
    service = StockUsDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_daily/clear")
async def clear_stock_us_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-新浪数据"""
    from app.services.stock.stock_us_daily_service import StockUsDailyService
    service = StockUsDailyService(db)
    return await service.clear_data()



# 知名美股 - stock_us_famous_spot_em
@router.get("/collections/stock_us_famous_spot_em")
async def get_stock_us_famous_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取知名美股数据"""
    from app.services.stock.stock_us_famous_spot_em_service import StockUsFamousSpotEmService
    service = StockUsFamousSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_famous_spot_em/overview")
async def get_stock_us_famous_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取知名美股数据概览"""
    from app.services.stock.stock_us_famous_spot_em_service import StockUsFamousSpotEmService
    service = StockUsFamousSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_famous_spot_em/refresh")
async def refresh_stock_us_famous_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新知名美股数据"""
    from app.services.stock.stock_us_famous_spot_em_service import StockUsFamousSpotEmService
    service = StockUsFamousSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_famous_spot_em/clear")
async def clear_stock_us_famous_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空知名美股数据"""
    from app.services.stock.stock_us_famous_spot_em_service import StockUsFamousSpotEmService
    service = StockUsFamousSpotEmService(db)
    return await service.clear_data()



# 历史行情数据-东财 - stock_us_hist
@router.get("/collections/stock_us_hist")
async def get_stock_us_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_hist/overview")
async def get_stock_us_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-东财数据概览"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_hist/refresh")
async def refresh_stock_us_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_hist/clear")
async def clear_stock_us_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-东财数据"""
    from app.services.stock.stock_us_hist_service import StockUsHistService
    service = StockUsHistService(db)
    return await service.clear_data()



# 分时数据-东财 - stock_us_hist_min_em
@router.get("/collections/stock_us_hist_min_em")
async def get_stock_us_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_hist_min_em/overview")
async def get_stock_us_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-东财数据概览"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_hist_min_em/refresh")
async def refresh_stock_us_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_hist_min_em/clear")
async def clear_stock_us_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据-东财数据"""
    from app.services.stock.stock_us_hist_min_em_service import StockUsHistMinEmService
    service = StockUsHistMinEmService(db)
    return await service.clear_data()



# 粉单市场 - stock_us_pink_spot_em
@router.get("/collections/stock_us_pink_spot_em")
async def get_stock_us_pink_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取粉单市场数据"""
    from app.services.stock.stock_us_pink_spot_em_service import StockUsPinkSpotEmService
    service = StockUsPinkSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_pink_spot_em/overview")
async def get_stock_us_pink_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取粉单市场数据概览"""
    from app.services.stock.stock_us_pink_spot_em_service import StockUsPinkSpotEmService
    service = StockUsPinkSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_pink_spot_em/refresh")
async def refresh_stock_us_pink_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新粉单市场数据"""
    from app.services.stock.stock_us_pink_spot_em_service import StockUsPinkSpotEmService
    service = StockUsPinkSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_pink_spot_em/clear")
async def clear_stock_us_pink_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空粉单市场数据"""
    from app.services.stock.stock_us_pink_spot_em_service import StockUsPinkSpotEmService
    service = StockUsPinkSpotEmService(db)
    return await service.clear_data()



# 实时行情数据-新浪 - stock_us_spot
@router.get("/collections/stock_us_spot")
async def get_stock_us_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据"""
    from app.services.stock.stock_us_spot_service import StockUsSpotService
    service = StockUsSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_spot/overview")
async def get_stock_us_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据概览"""
    from app.services.stock.stock_us_spot_service import StockUsSpotService
    service = StockUsSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_spot/refresh")
async def refresh_stock_us_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-新浪数据"""
    from app.services.stock.stock_us_spot_service import StockUsSpotService
    service = StockUsSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_spot/clear")
async def clear_stock_us_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-新浪数据"""
    from app.services.stock.stock_us_spot_service import StockUsSpotService
    service = StockUsSpotService(db)
    return await service.clear_data()



# 实时行情数据-东财 - stock_us_spot_em
@router.get("/collections/stock_us_spot_em")
async def get_stock_us_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据"""
    from app.services.stock.stock_us_spot_em_service import StockUsSpotEmService
    service = StockUsSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_us_spot_em/overview")
async def get_stock_us_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据概览"""
    from app.services.stock.stock_us_spot_em_service import StockUsSpotEmService
    service = StockUsSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_us_spot_em/refresh")
async def refresh_stock_us_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-东财数据"""
    from app.services.stock.stock_us_spot_em_service import StockUsSpotEmService
    service = StockUsSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_us_spot_em/clear")
async def clear_stock_us_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-东财数据"""
    from app.services.stock.stock_us_spot_em_service import StockUsSpotEmService
    service = StockUsSpotEmService(db)
    return await service.clear_data()



# 个股估值 - stock_value_em
@router.get("/collections/stock_value_em")
async def get_stock_value_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股估值数据"""
    from app.services.stock.stock_value_em_service import StockValueEmService
    service = StockValueEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_value_em/overview")
async def get_stock_value_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取个股估值数据概览"""
    from app.services.stock.stock_value_em_service import StockValueEmService
    service = StockValueEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_value_em/refresh")
async def refresh_stock_value_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新个股估值数据"""
    from app.services.stock.stock_value_em_service import StockValueEmService
    service = StockValueEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_value_em/clear")
async def clear_stock_value_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空个股估值数据"""
    from app.services.stock.stock_value_em_service import StockValueEmService
    service = StockValueEmService(db)
    return await service.clear_data()



# 新股上市首日 - stock_xgsr_ths
@router.get("/collections/stock_xgsr_ths")
async def get_stock_xgsr_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_xgsr_ths/overview")
async def get_stock_xgsr_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股上市首日数据概览"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_xgsr_ths/refresh")
async def refresh_stock_xgsr_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_xgsr_ths/clear")
async def clear_stock_xgsr_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股上市首日数据"""
    from app.services.stock.stock_xgsr_ths_service import StockXgsrThsService
    service = StockXgsrThsService(db)
    return await service.clear_data()



# 现金流量表 - stock_xjll_em
@router.get("/collections/stock_xjll_em")
async def get_stock_xjll_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取现金流量表数据"""
    from app.services.stock.stock_xjll_em_service import StockXjllEmService
    service = StockXjllEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_xjll_em/overview")
async def get_stock_xjll_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取现金流量表数据概览"""
    from app.services.stock.stock_xjll_em_service import StockXjllEmService
    service = StockXjllEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_xjll_em/refresh")
async def refresh_stock_xjll_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新现金流量表数据"""
    from app.services.stock.stock_xjll_em_service import StockXjllEmService
    service = StockXjllEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_xjll_em/clear")
async def clear_stock_xjll_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空现金流量表数据"""
    from app.services.stock.stock_xjll_em_service import StockXjllEmService
    service = StockXjllEmService(db)
    return await service.clear_data()



# 业绩报表 - stock_yjbb_em
@router.get("/collections/stock_yjbb_em")
async def get_stock_yjbb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_yjbb_em/overview")
async def get_stock_yjbb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩报表数据概览"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_yjbb_em/refresh")
async def refresh_stock_yjbb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_yjbb_em/clear")
async def clear_stock_yjbb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空业绩报表数据"""
    from app.services.stock.stock_yjbb_em_service import StockYjbbEmService
    service = StockYjbbEmService(db)
    return await service.clear_data()



# 业绩快报 - stock_yjkb_em
@router.get("/collections/stock_yjkb_em")
async def get_stock_yjkb_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_yjkb_em/overview")
async def get_stock_yjkb_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取业绩快报数据概览"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_yjkb_em/refresh")
async def refresh_stock_yjkb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_yjkb_em/clear")
async def clear_stock_yjkb_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空业绩快报数据"""
    from app.services.stock.stock_yjkb_em_service import StockYjkbEmService
    service = StockYjkbEmService(db)
    return await service.clear_data()



# 一致行动人 - stock_yzxdr_em
@router.get("/collections/stock_yzxdr_em")
async def get_stock_yzxdr_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取一致行动人数据"""
    from app.services.stock.stock_yzxdr_em_service import StockYzxdrEmService
    service = StockYzxdrEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_yzxdr_em/overview")
async def get_stock_yzxdr_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取一致行动人数据概览"""
    from app.services.stock.stock_yzxdr_em_service import StockYzxdrEmService
    service = StockYzxdrEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_yzxdr_em/refresh")
async def refresh_stock_yzxdr_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新一致行动人数据"""
    from app.services.stock.stock_yzxdr_em_service import StockYzxdrEmService
    service = StockYzxdrEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_yzxdr_em/clear")
async def clear_stock_yzxdr_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空一致行动人数据"""
    from app.services.stock.stock_yzxdr_em_service import StockYzxdrEmService
    service = StockYzxdrEmService(db)
    return await service.clear_data()



# 资产负债表-北交所 - stock_zcfz_bj_em
@router.get("/collections/stock_zcfz_bj_em")
async def get_stock_zcfz_bj_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-北交所数据"""
    from app.services.stock.stock_zcfz_bj_em_service import StockZcfzBjEmService
    service = StockZcfzBjEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zcfz_bj_em/overview")
async def get_stock_zcfz_bj_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-北交所数据概览"""
    from app.services.stock.stock_zcfz_bj_em_service import StockZcfzBjEmService
    service = StockZcfzBjEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zcfz_bj_em/refresh")
async def refresh_stock_zcfz_bj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新资产负债表-北交所数据"""
    from app.services.stock.stock_zcfz_bj_em_service import StockZcfzBjEmService
    service = StockZcfzBjEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zcfz_bj_em/clear")
async def clear_stock_zcfz_bj_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空资产负债表-北交所数据"""
    from app.services.stock.stock_zcfz_bj_em_service import StockZcfzBjEmService
    service = StockZcfzBjEmService(db)
    return await service.clear_data()



# 资产负债表-沪深 - stock_zcfz_em
@router.get("/collections/stock_zcfz_em")
async def get_stock_zcfz_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zcfz_em/overview")
async def get_stock_zcfz_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取资产负债表-沪深数据概览"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zcfz_em/refresh")
async def refresh_stock_zcfz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zcfz_em/clear")
async def clear_stock_zcfz_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空资产负债表-沪深数据"""
    from app.services.stock.stock_zcfz_em_service import StockZcfzEmService
    service = StockZcfzEmService(db)
    return await service.clear_data()



# 历史行情数据 - stock_zh_a_cdr_daily
@router.get("/collections/stock_zh_a_cdr_daily")
async def get_stock_zh_a_cdr_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据"""
    from app.services.stock.stock_zh_a_cdr_daily_service import StockZhACdrDailyService
    service = StockZhACdrDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_cdr_daily/overview")
async def get_stock_zh_a_cdr_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据概览"""
    from app.services.stock.stock_zh_a_cdr_daily_service import StockZhACdrDailyService
    service = StockZhACdrDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_cdr_daily/refresh")
async def refresh_stock_zh_a_cdr_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据数据"""
    from app.services.stock.stock_zh_a_cdr_daily_service import StockZhACdrDailyService
    service = StockZhACdrDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_cdr_daily/clear")
async def clear_stock_zh_a_cdr_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据数据"""
    from app.services.stock.stock_zh_a_cdr_daily_service import StockZhACdrDailyService
    service = StockZhACdrDailyService(db)
    return await service.clear_data()



# 历史行情数据-新浪 - stock_zh_a_daily
@router.get("/collections/stock_zh_a_daily")
async def get_stock_zh_a_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_daily_service import StockZhADailyService
    service = StockZhADailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_daily/overview")
async def get_stock_zh_a_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-新浪数据概览"""
    from app.services.stock.stock_zh_a_daily_service import StockZhADailyService
    service = StockZhADailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_daily/refresh")
async def refresh_stock_zh_a_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_daily_service import StockZhADailyService
    service = StockZhADailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_daily/clear")
async def clear_stock_zh_a_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_daily_service import StockZhADailyService
    service = StockZhADailyService(db)
    return await service.clear_data()



# 信息披露调研-巨潮资讯 - stock_zh_a_disclosure_relation_cninfo
@router.get("/collections/stock_zh_a_disclosure_relation_cninfo")
async def get_stock_zh_a_disclosure_relation_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_disclosure_relation_cninfo/overview")
async def get_stock_zh_a_disclosure_relation_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露调研-巨潮资讯数据概览"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_disclosure_relation_cninfo/refresh")
async def refresh_stock_zh_a_disclosure_relation_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_disclosure_relation_cninfo/clear")
async def clear_stock_zh_a_disclosure_relation_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空信息披露调研-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_relation_cninfo_service import StockZhADisclosureRelationCninfoService
    service = StockZhADisclosureRelationCninfoService(db)
    return await service.clear_data()



# 信息披露公告-巨潮资讯 - stock_zh_a_disclosure_report_cninfo
@router.get("/collections/stock_zh_a_disclosure_report_cninfo")
async def get_stock_zh_a_disclosure_report_cninfo(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露公告-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_report_cninfo_service import StockZhADisclosureReportCninfoService
    service = StockZhADisclosureReportCninfoService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_disclosure_report_cninfo/overview")
async def get_stock_zh_a_disclosure_report_cninfo_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取信息披露公告-巨潮资讯数据概览"""
    from app.services.stock.stock_zh_a_disclosure_report_cninfo_service import StockZhADisclosureReportCninfoService
    service = StockZhADisclosureReportCninfoService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_disclosure_report_cninfo/refresh")
async def refresh_stock_zh_a_disclosure_report_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新信息披露公告-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_report_cninfo_service import StockZhADisclosureReportCninfoService
    service = StockZhADisclosureReportCninfoService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_disclosure_report_cninfo/clear")
async def clear_stock_zh_a_disclosure_report_cninfo(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空信息披露公告-巨潮资讯数据"""
    from app.services.stock.stock_zh_a_disclosure_report_cninfo_service import StockZhADisclosureReportCninfoService
    service = StockZhADisclosureReportCninfoService(db)
    return await service.clear_data()



# 股本结构 - stock_zh_a_gbjg_em
@router.get("/collections/stock_zh_a_gbjg_em")
async def get_stock_zh_a_gbjg_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_gbjg_em/overview")
async def get_stock_zh_a_gbjg_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股本结构数据概览"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_gbjg_em/refresh")
async def refresh_stock_zh_a_gbjg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_gbjg_em/clear")
async def clear_stock_zh_a_gbjg_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股本结构数据"""
    from app.services.stock.stock_zh_a_gbjg_em_service import StockZhAGbjgEmService
    service = StockZhAGbjgEmService(db)
    return await service.clear_data()



# 股东户数 - stock_zh_a_gdhs
@router.get("/collections/stock_zh_a_gdhs")
async def get_stock_zh_a_gdhs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_gdhs/overview")
async def get_stock_zh_a_gdhs_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数数据概览"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_gdhs/refresh")
async def refresh_stock_zh_a_gdhs(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_gdhs/clear")
async def clear_stock_zh_a_gdhs(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东户数数据"""
    from app.services.stock.stock_zh_a_gdhs_service import StockZhAGdhsService
    service = StockZhAGdhsService(db)
    return await service.clear_data()



# 股东户数详情 - stock_zh_a_gdhs_detail_em
@router.get("/collections/stock_zh_a_gdhs_detail_em")
async def get_stock_zh_a_gdhs_detail_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数详情数据"""
    from app.services.stock.stock_zh_a_gdhs_detail_em_service import StockZhAGdhsDetailEmService
    service = StockZhAGdhsDetailEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_gdhs_detail_em/overview")
async def get_stock_zh_a_gdhs_detail_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取股东户数详情数据概览"""
    from app.services.stock.stock_zh_a_gdhs_detail_em_service import StockZhAGdhsDetailEmService
    service = StockZhAGdhsDetailEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_gdhs_detail_em/refresh")
async def refresh_stock_zh_a_gdhs_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新股东户数详情数据"""
    from app.services.stock.stock_zh_a_gdhs_detail_em_service import StockZhAGdhsDetailEmService
    service = StockZhAGdhsDetailEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_gdhs_detail_em/clear")
async def clear_stock_zh_a_gdhs_detail_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空股东户数详情数据"""
    from app.services.stock.stock_zh_a_gdhs_detail_em_service import StockZhAGdhsDetailEmService
    service = StockZhAGdhsDetailEmService(db)
    return await service.clear_data()



# A股历史行情-东财 - stock_zh_a_hist
@router.get("/collections/stock_zh_a_hist")
async def get_stock_zh_a_hist(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist/overview")
async def get_stock_zh_a_hist_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股历史行情-东财数据概览"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist/refresh")
async def refresh_stock_zh_a_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist/clear")
async def clear_stock_zh_a_hist(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股历史行情-东财数据"""
    from app.services.stock.stock_zh_a_hist_service import StockZhAHistService
    service = StockZhAHistService(db)
    return await service.clear_data()



# A股分时数据-东财 - stock_zh_a_hist_min_em
@router.get("/collections/stock_zh_a_hist_min_em")
async def get_stock_zh_a_hist_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股分时数据-东财数据"""
    from app.services.stock.stock_zh_a_hist_min_em_service import StockZhAHistMinEmService
    service = StockZhAHistMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist_min_em/overview")
async def get_stock_zh_a_hist_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A股分时数据-东财数据概览"""
    from app.services.stock.stock_zh_a_hist_min_em_service import StockZhAHistMinEmService
    service = StockZhAHistMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist_min_em/refresh")
async def refresh_stock_zh_a_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A股分时数据-东财数据"""
    from app.services.stock.stock_zh_a_hist_min_em_service import StockZhAHistMinEmService
    service = StockZhAHistMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist_min_em/clear")
async def clear_stock_zh_a_hist_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A股分时数据-东财数据"""
    from app.services.stock.stock_zh_a_hist_min_em_service import StockZhAHistMinEmService
    service = StockZhAHistMinEmService(db)
    return await service.clear_data()



# 盘前数据 - stock_zh_a_hist_pre_min_em
@router.get("/collections/stock_zh_a_hist_pre_min_em")
async def get_stock_zh_a_hist_pre_min_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘前数据数据"""
    from app.services.stock.stock_zh_a_hist_pre_min_em_service import StockZhAHistPreMinEmService
    service = StockZhAHistPreMinEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist_pre_min_em/overview")
async def get_stock_zh_a_hist_pre_min_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取盘前数据数据概览"""
    from app.services.stock.stock_zh_a_hist_pre_min_em_service import StockZhAHistPreMinEmService
    service = StockZhAHistPreMinEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist_pre_min_em/refresh")
async def refresh_stock_zh_a_hist_pre_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新盘前数据数据"""
    from app.services.stock.stock_zh_a_hist_pre_min_em_service import StockZhAHistPreMinEmService
    service = StockZhAHistPreMinEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist_pre_min_em/clear")
async def clear_stock_zh_a_hist_pre_min_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空盘前数据数据"""
    from app.services.stock.stock_zh_a_hist_pre_min_em_service import StockZhAHistPreMinEmService
    service = StockZhAHistPreMinEmService(db)
    return await service.clear_data()



# 历史行情数据-腾讯 - stock_zh_a_hist_tx
@router.get("/collections/stock_zh_a_hist_tx")
async def get_stock_zh_a_hist_tx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_hist_tx/overview")
async def get_stock_zh_a_hist_tx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据-腾讯数据概览"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_hist_tx/refresh")
async def refresh_stock_zh_a_hist_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_hist_tx/clear")
async def clear_stock_zh_a_hist_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据-腾讯数据"""
    from app.services.stock.stock_zh_a_hist_tx_service import StockZhAHistTxService
    service = StockZhAHistTxService(db)
    return await service.clear_data()



# 分时数据-新浪 - stock_zh_a_minute
@router.get("/collections/stock_zh_a_minute")
async def get_stock_zh_a_minute(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_minute/overview")
async def get_stock_zh_a_minute_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据-新浪数据概览"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_minute/refresh")
async def refresh_stock_zh_a_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_minute/clear")
async def clear_stock_zh_a_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据-新浪数据"""
    from app.services.stock.stock_zh_a_minute_service import StockZhAMinuteService
    service = StockZhAMinuteService(db)
    return await service.clear_data()



# 新股 - stock_zh_a_new_em
@router.get("/collections/stock_zh_a_new_em")
async def get_stock_zh_a_new_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股数据"""
    from app.services.stock.stock_zh_a_new_em_service import StockZhANewEmService
    service = StockZhANewEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_new_em/overview")
async def get_stock_zh_a_new_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取新股数据概览"""
    from app.services.stock.stock_zh_a_new_em_service import StockZhANewEmService
    service = StockZhANewEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_new_em/refresh")
async def refresh_stock_zh_a_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新新股数据"""
    from app.services.stock.stock_zh_a_new_em_service import StockZhANewEmService
    service = StockZhANewEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_new_em/clear")
async def clear_stock_zh_a_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空新股数据"""
    from app.services.stock.stock_zh_a_new_em_service import StockZhANewEmService
    service = StockZhANewEmService(db)
    return await service.clear_data()



# 实时行情数据-新浪 - stock_zh_a_spot
@router.get("/collections/stock_zh_a_spot")
async def get_stock_zh_a_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_spot_service import StockZhASpotService
    service = StockZhASpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_spot/overview")
async def get_stock_zh_a_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据概览"""
    from app.services.stock.stock_zh_a_spot_service import StockZhASpotService
    service = StockZhASpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_spot/refresh")
async def refresh_stock_zh_a_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_spot_service import StockZhASpotService
    service = StockZhASpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_spot/clear")
async def clear_stock_zh_a_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_a_spot_service import StockZhASpotService
    service = StockZhASpotService(db)
    return await service.clear_data()



# 沪深京A股实时行情-东财 - stock_zh_a_spot_em
@router.get("/collections/stock_zh_a_spot_em")
async def get_stock_zh_a_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_spot_em/overview")
async def get_stock_zh_a_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取沪深京A股实时行情-东财数据概览"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_spot_em/refresh")
async def refresh_stock_zh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_spot_em/clear")
async def clear_stock_zh_a_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空沪深京A股实时行情-东财数据"""
    from app.services.stock.stock_zh_a_spot_em_service import StockZhASpotEmService
    service = StockZhASpotEmService(db)
    return await service.clear_data()



# 风险警示板 - stock_zh_a_st_em
@router.get("/collections/stock_zh_a_st_em")
async def get_stock_zh_a_st_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_st_em/overview")
async def get_stock_zh_a_st_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取风险警示板数据概览"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_st_em/refresh")
async def refresh_stock_zh_a_st_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_st_em/clear")
async def clear_stock_zh_a_st_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空风险警示板数据"""
    from app.services.stock.stock_zh_a_st_em_service import StockZhAStEmService
    service = StockZhAStEmService(db)
    return await service.clear_data()



# 两网及退市 - stock_zh_a_stop_em
@router.get("/collections/stock_zh_a_stop_em")
async def get_stock_zh_a_stop_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_stop_em/overview")
async def get_stock_zh_a_stop_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取两网及退市数据概览"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_stop_em/refresh")
async def refresh_stock_zh_a_stop_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_stop_em/clear")
async def clear_stock_zh_a_stop_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空两网及退市数据"""
    from app.services.stock.stock_zh_a_stop_em_service import StockZhAStopEmService
    service = StockZhAStopEmService(db)
    return await service.clear_data()



# 腾讯财经 - stock_zh_a_tick_tx
@router.get("/collections/stock_zh_a_tick_tx")
async def get_stock_zh_a_tick_tx(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_a_tick_tx/overview")
async def get_stock_zh_a_tick_tx_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取腾讯财经数据概览"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_a_tick_tx/refresh")
async def refresh_stock_zh_a_tick_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_a_tick_tx/clear")
async def clear_stock_zh_a_tick_tx(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空腾讯财经数据"""
    from app.services.stock.stock_zh_a_tick_tx_service import StockZhATickTxService
    service = StockZhATickTxService(db)
    return await service.clear_data()



# AB 股比价 - stock_zh_ab_comparison_em
@router.get("/collections/stock_zh_ab_comparison_em")
async def get_stock_zh_ab_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取AB 股比价数据"""
    from app.services.stock.stock_zh_ab_comparison_em_service import StockZhAbComparisonEmService
    service = StockZhAbComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ab_comparison_em/overview")
async def get_stock_zh_ab_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取AB 股比价数据概览"""
    from app.services.stock.stock_zh_ab_comparison_em_service import StockZhAbComparisonEmService
    service = StockZhAbComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ab_comparison_em/refresh")
async def refresh_stock_zh_ab_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新AB 股比价数据"""
    from app.services.stock.stock_zh_ab_comparison_em_service import StockZhAbComparisonEmService
    service = StockZhAbComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ab_comparison_em/clear")
async def clear_stock_zh_ab_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空AB 股比价数据"""
    from app.services.stock.stock_zh_ab_comparison_em_service import StockZhAbComparisonEmService
    service = StockZhAbComparisonEmService(db)
    return await service.clear_data()



# 历史行情数据 - stock_zh_ah_daily
@router.get("/collections/stock_zh_ah_daily")
async def get_stock_zh_ah_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_daily/overview")
async def get_stock_zh_ah_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据概览"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_daily/refresh")
async def refresh_stock_zh_ah_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_daily/clear")
async def clear_stock_zh_ah_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据数据"""
    from app.services.stock.stock_zh_ah_daily_service import StockZhAhDailyService
    service = StockZhAhDailyService(db)
    return await service.clear_data()



# A+H股票字典 - stock_zh_ah_name
@router.get("/collections/stock_zh_ah_name")
async def get_stock_zh_ah_name(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_name/overview")
async def get_stock_zh_ah_name_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A+H股票字典数据概览"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_name/refresh")
async def refresh_stock_zh_ah_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_name/clear")
async def clear_stock_zh_ah_name(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A+H股票字典数据"""
    from app.services.stock.stock_zh_ah_name_service import StockZhAhNameService
    service = StockZhAhNameService(db)
    return await service.clear_data()



# 实时行情数据-腾讯 - stock_zh_ah_spot
@router.get("/collections/stock_zh_ah_spot")
async def get_stock_zh_ah_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_spot/overview")
async def get_stock_zh_ah_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-腾讯数据概览"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_spot/refresh")
async def refresh_stock_zh_ah_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_spot/clear")
async def clear_stock_zh_ah_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-腾讯数据"""
    from app.services.stock.stock_zh_ah_spot_service import StockZhAhSpotService
    service = StockZhAhSpotService(db)
    return await service.clear_data()



# 实时行情数据-东财 - stock_zh_ah_spot_em
@router.get("/collections/stock_zh_ah_spot_em")
async def get_stock_zh_ah_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据"""
    from app.services.stock.stock_zh_ah_spot_em_service import StockZhAhSpotEmService
    service = StockZhAhSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_ah_spot_em/overview")
async def get_stock_zh_ah_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据概览"""
    from app.services.stock.stock_zh_ah_spot_em_service import StockZhAhSpotEmService
    service = StockZhAhSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_ah_spot_em/refresh")
async def refresh_stock_zh_ah_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-东财数据"""
    from app.services.stock.stock_zh_ah_spot_em_service import StockZhAhSpotEmService
    service = StockZhAhSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_ah_spot_em/clear")
async def clear_stock_zh_ah_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-东财数据"""
    from app.services.stock.stock_zh_ah_spot_em_service import StockZhAhSpotEmService
    service = StockZhAhSpotEmService(db)
    return await service.clear_data()



# 历史行情数据 - stock_zh_b_daily
@router.get("/collections/stock_zh_b_daily")
async def get_stock_zh_b_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据"""
    from app.services.stock.stock_zh_b_daily_service import StockZhBDailyService
    service = StockZhBDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_b_daily/overview")
async def get_stock_zh_b_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据概览"""
    from app.services.stock.stock_zh_b_daily_service import StockZhBDailyService
    service = StockZhBDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_b_daily/refresh")
async def refresh_stock_zh_b_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据数据"""
    from app.services.stock.stock_zh_b_daily_service import StockZhBDailyService
    service = StockZhBDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_b_daily/clear")
async def clear_stock_zh_b_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据数据"""
    from app.services.stock.stock_zh_b_daily_service import StockZhBDailyService
    service = StockZhBDailyService(db)
    return await service.clear_data()



# 分时数据 - stock_zh_b_minute
@router.get("/collections/stock_zh_b_minute")
async def get_stock_zh_b_minute(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_b_minute/overview")
async def get_stock_zh_b_minute_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取分时数据数据概览"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_b_minute/refresh")
async def refresh_stock_zh_b_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_b_minute/clear")
async def clear_stock_zh_b_minute(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空分时数据数据"""
    from app.services.stock.stock_zh_b_minute_service import StockZhBMinuteService
    service = StockZhBMinuteService(db)
    return await service.clear_data()



# 实时行情数据-新浪 - stock_zh_b_spot
@router.get("/collections/stock_zh_b_spot")
async def get_stock_zh_b_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_b_spot_service import StockZhBSpotService
    service = StockZhBSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_b_spot/overview")
async def get_stock_zh_b_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-新浪数据概览"""
    from app.services.stock.stock_zh_b_spot_service import StockZhBSpotService
    service = StockZhBSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_b_spot/refresh")
async def refresh_stock_zh_b_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_b_spot_service import StockZhBSpotService
    service = StockZhBSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_b_spot/clear")
async def clear_stock_zh_b_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-新浪数据"""
    from app.services.stock.stock_zh_b_spot_service import StockZhBSpotService
    service = StockZhBSpotService(db)
    return await service.clear_data()



# 实时行情数据-东财 - stock_zh_b_spot_em
@router.get("/collections/stock_zh_b_spot_em")
async def get_stock_zh_b_spot_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据"""
    from app.services.stock.stock_zh_b_spot_em_service import StockZhBSpotEmService
    service = StockZhBSpotEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_b_spot_em/overview")
async def get_stock_zh_b_spot_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据-东财数据概览"""
    from app.services.stock.stock_zh_b_spot_em_service import StockZhBSpotEmService
    service = StockZhBSpotEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_b_spot_em/refresh")
async def refresh_stock_zh_b_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据-东财数据"""
    from app.services.stock.stock_zh_b_spot_em_service import StockZhBSpotEmService
    service = StockZhBSpotEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_b_spot_em/clear")
async def clear_stock_zh_b_spot_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据-东财数据"""
    from app.services.stock.stock_zh_b_spot_em_service import StockZhBSpotEmService
    service = StockZhBSpotEmService(db)
    return await service.clear_data()



# 杜邦分析比较 - stock_zh_dupont_comparison_em
@router.get("/collections/stock_zh_dupont_comparison_em")
async def get_stock_zh_dupont_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取杜邦分析比较数据"""
    from app.services.stock.stock_zh_dupont_comparison_em_service import StockZhDupontComparisonEmService
    service = StockZhDupontComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_dupont_comparison_em/overview")
async def get_stock_zh_dupont_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取杜邦分析比较数据概览"""
    from app.services.stock.stock_zh_dupont_comparison_em_service import StockZhDupontComparisonEmService
    service = StockZhDupontComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_dupont_comparison_em/refresh")
async def refresh_stock_zh_dupont_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新杜邦分析比较数据"""
    from app.services.stock.stock_zh_dupont_comparison_em_service import StockZhDupontComparisonEmService
    service = StockZhDupontComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_dupont_comparison_em/clear")
async def clear_stock_zh_dupont_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空杜邦分析比较数据"""
    from app.services.stock.stock_zh_dupont_comparison_em_service import StockZhDupontComparisonEmService
    service = StockZhDupontComparisonEmService(db)
    return await service.clear_data()



# 成长性比较 - stock_zh_growth_comparison_em
@router.get("/collections/stock_zh_growth_comparison_em")
async def get_stock_zh_growth_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取成长性比较数据"""
    from app.services.stock.stock_zh_growth_comparison_em_service import StockZhGrowthComparisonEmService
    service = StockZhGrowthComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_growth_comparison_em/overview")
async def get_stock_zh_growth_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取成长性比较数据概览"""
    from app.services.stock.stock_zh_growth_comparison_em_service import StockZhGrowthComparisonEmService
    service = StockZhGrowthComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_growth_comparison_em/refresh")
async def refresh_stock_zh_growth_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新成长性比较数据"""
    from app.services.stock.stock_zh_growth_comparison_em_service import StockZhGrowthComparisonEmService
    service = StockZhGrowthComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_growth_comparison_em/clear")
async def clear_stock_zh_growth_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空成长性比较数据"""
    from app.services.stock.stock_zh_growth_comparison_em_service import StockZhGrowthComparisonEmService
    service = StockZhGrowthComparisonEmService(db)
    return await service.clear_data()



# 历史行情数据 - stock_zh_kcb_daily
@router.get("/collections/stock_zh_kcb_daily")
async def get_stock_zh_kcb_daily(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据"""
    from app.services.stock.stock_zh_kcb_daily_service import StockZhKcbDailyService
    service = StockZhKcbDailyService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_kcb_daily/overview")
async def get_stock_zh_kcb_daily_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取历史行情数据数据概览"""
    from app.services.stock.stock_zh_kcb_daily_service import StockZhKcbDailyService
    service = StockZhKcbDailyService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_kcb_daily/refresh")
async def refresh_stock_zh_kcb_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新历史行情数据数据"""
    from app.services.stock.stock_zh_kcb_daily_service import StockZhKcbDailyService
    service = StockZhKcbDailyService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_kcb_daily/clear")
async def clear_stock_zh_kcb_daily(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空历史行情数据数据"""
    from app.services.stock.stock_zh_kcb_daily_service import StockZhKcbDailyService
    service = StockZhKcbDailyService(db)
    return await service.clear_data()



# 科创板公告 - stock_zh_kcb_report_em
@router.get("/collections/stock_zh_kcb_report_em")
async def get_stock_zh_kcb_report_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_kcb_report_em/overview")
async def get_stock_zh_kcb_report_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取科创板公告数据概览"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_kcb_report_em/refresh")
async def refresh_stock_zh_kcb_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_kcb_report_em/clear")
async def clear_stock_zh_kcb_report_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空科创板公告数据"""
    from app.services.stock.stock_zh_kcb_report_em_service import StockZhKcbReportEmService
    service = StockZhKcbReportEmService(db)
    return await service.clear_data()



# 实时行情数据 - stock_zh_kcb_spot
@router.get("/collections/stock_zh_kcb_spot")
async def get_stock_zh_kcb_spot(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_kcb_spot/overview")
async def get_stock_zh_kcb_spot_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取实时行情数据数据概览"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_kcb_spot/refresh")
async def refresh_stock_zh_kcb_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_kcb_spot/clear")
async def clear_stock_zh_kcb_spot(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空实时行情数据数据"""
    from app.services.stock.stock_zh_kcb_spot_service import StockZhKcbSpotService
    service = StockZhKcbSpotService(db)
    return await service.clear_data()



# 公司规模 - stock_zh_scale_comparison_em
@router.get("/collections/stock_zh_scale_comparison_em")
async def get_stock_zh_scale_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司规模数据"""
    from app.services.stock.stock_zh_scale_comparison_em_service import StockZhScaleComparisonEmService
    service = StockZhScaleComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_scale_comparison_em/overview")
async def get_stock_zh_scale_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取公司规模数据概览"""
    from app.services.stock.stock_zh_scale_comparison_em_service import StockZhScaleComparisonEmService
    service = StockZhScaleComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_scale_comparison_em/refresh")
async def refresh_stock_zh_scale_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新公司规模数据"""
    from app.services.stock.stock_zh_scale_comparison_em_service import StockZhScaleComparisonEmService
    service = StockZhScaleComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_scale_comparison_em/clear")
async def clear_stock_zh_scale_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空公司规模数据"""
    from app.services.stock.stock_zh_scale_comparison_em_service import StockZhScaleComparisonEmService
    service = StockZhScaleComparisonEmService(db)
    return await service.clear_data()



# A 股估值指标 - stock_zh_valuation_baidu
@router.get("/collections/stock_zh_valuation_baidu")
async def get_stock_zh_valuation_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_valuation_baidu/overview")
async def get_stock_zh_valuation_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取A 股估值指标数据概览"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_valuation_baidu/refresh")
async def refresh_stock_zh_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_valuation_baidu/clear")
async def clear_stock_zh_valuation_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空A 股估值指标数据"""
    from app.services.stock.stock_zh_valuation_baidu_service import StockZhValuationBaiduService
    service = StockZhValuationBaiduService(db)
    return await service.clear_data()



# 估值比较 - stock_zh_valuation_comparison_em
@router.get("/collections/stock_zh_valuation_comparison_em")
async def get_stock_zh_valuation_comparison_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_valuation_comparison_em/overview")
async def get_stock_zh_valuation_comparison_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取估值比较数据概览"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_valuation_comparison_em/refresh")
async def refresh_stock_zh_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_valuation_comparison_em/clear")
async def clear_stock_zh_valuation_comparison_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空估值比较数据"""
    from app.services.stock.stock_zh_valuation_comparison_em_service import StockZhValuationComparisonEmService
    service = StockZhValuationComparisonEmService(db)
    return await service.clear_data()



# 涨跌投票 - stock_zh_vote_baidu
@router.get("/collections/stock_zh_vote_baidu")
async def get_stock_zh_vote_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zh_vote_baidu/overview")
async def get_stock_zh_vote_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨跌投票数据概览"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.get_overview()


@router.post("/collections/stock_zh_vote_baidu/refresh")
async def refresh_stock_zh_vote_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zh_vote_baidu/clear")
async def clear_stock_zh_vote_baidu(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空涨跌投票数据"""
    from app.services.stock.stock_zh_vote_baidu_service import StockZhVoteBaiduService
    service = StockZhVoteBaiduService(db)
    return await service.clear_data()



# 跌停股池 - stock_zt_pool_dtgc_em
@router.get("/collections/stock_zt_pool_dtgc_em")
async def get_stock_zt_pool_dtgc_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取跌停股池数据"""
    from app.services.stock.stock_zt_pool_dtgc_em_service import StockZtPoolDtgcEmService
    service = StockZtPoolDtgcEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_dtgc_em/overview")
async def get_stock_zt_pool_dtgc_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取跌停股池数据概览"""
    from app.services.stock.stock_zt_pool_dtgc_em_service import StockZtPoolDtgcEmService
    service = StockZtPoolDtgcEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_dtgc_em/refresh")
async def refresh_stock_zt_pool_dtgc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新跌停股池数据"""
    from app.services.stock.stock_zt_pool_dtgc_em_service import StockZtPoolDtgcEmService
    service = StockZtPoolDtgcEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_dtgc_em/clear")
async def clear_stock_zt_pool_dtgc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空跌停股池数据"""
    from app.services.stock.stock_zt_pool_dtgc_em_service import StockZtPoolDtgcEmService
    service = StockZtPoolDtgcEmService(db)
    return await service.clear_data()



# 涨停股池 - stock_zt_pool_em
@router.get("/collections/stock_zt_pool_em")
async def get_stock_zt_pool_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨停股池数据"""
    from app.services.stock.stock_zt_pool_em_service import StockZtPoolEmService
    service = StockZtPoolEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_em/overview")
async def get_stock_zt_pool_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取涨停股池数据概览"""
    from app.services.stock.stock_zt_pool_em_service import StockZtPoolEmService
    service = StockZtPoolEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_em/refresh")
async def refresh_stock_zt_pool_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新涨停股池数据"""
    from app.services.stock.stock_zt_pool_em_service import StockZtPoolEmService
    service = StockZtPoolEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_em/clear")
async def clear_stock_zt_pool_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空涨停股池数据"""
    from app.services.stock.stock_zt_pool_em_service import StockZtPoolEmService
    service = StockZtPoolEmService(db)
    return await service.clear_data()



# 昨日涨停股池 - stock_zt_pool_previous_em
@router.get("/collections/stock_zt_pool_previous_em")
async def get_stock_zt_pool_previous_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_previous_em/overview")
async def get_stock_zt_pool_previous_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取昨日涨停股池数据概览"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_previous_em/refresh")
async def refresh_stock_zt_pool_previous_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_previous_em/clear")
async def clear_stock_zt_pool_previous_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空昨日涨停股池数据"""
    from app.services.stock.stock_zt_pool_previous_em_service import StockZtPoolPreviousEmService
    service = StockZtPoolPreviousEmService(db)
    return await service.clear_data()



# 强势股池 - stock_zt_pool_strong_em
@router.get("/collections/stock_zt_pool_strong_em")
async def get_stock_zt_pool_strong_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取强势股池数据"""
    from app.services.stock.stock_zt_pool_strong_em_service import StockZtPoolStrongEmService
    service = StockZtPoolStrongEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_strong_em/overview")
async def get_stock_zt_pool_strong_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取强势股池数据概览"""
    from app.services.stock.stock_zt_pool_strong_em_service import StockZtPoolStrongEmService
    service = StockZtPoolStrongEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_strong_em/refresh")
async def refresh_stock_zt_pool_strong_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新强势股池数据"""
    from app.services.stock.stock_zt_pool_strong_em_service import StockZtPoolStrongEmService
    service = StockZtPoolStrongEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_strong_em/clear")
async def clear_stock_zt_pool_strong_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空强势股池数据"""
    from app.services.stock.stock_zt_pool_strong_em_service import StockZtPoolStrongEmService
    service = StockZtPoolStrongEmService(db)
    return await service.clear_data()



# 次新股池 - stock_zt_pool_sub_new_em
@router.get("/collections/stock_zt_pool_sub_new_em")
async def get_stock_zt_pool_sub_new_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_sub_new_em/overview")
async def get_stock_zt_pool_sub_new_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取次新股池数据概览"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_sub_new_em/refresh")
async def refresh_stock_zt_pool_sub_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_sub_new_em/clear")
async def clear_stock_zt_pool_sub_new_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空次新股池数据"""
    from app.services.stock.stock_zt_pool_sub_new_em_service import StockZtPoolSubNewEmService
    service = StockZtPoolSubNewEmService(db)
    return await service.clear_data()



# 炸板股池 - stock_zt_pool_zbgc_em
@router.get("/collections/stock_zt_pool_zbgc_em")
async def get_stock_zt_pool_zbgc_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取炸板股池数据"""
    from app.services.stock.stock_zt_pool_zbgc_em_service import StockZtPoolZbgcEmService
    service = StockZtPoolZbgcEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zt_pool_zbgc_em/overview")
async def get_stock_zt_pool_zbgc_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取炸板股池数据概览"""
    from app.services.stock.stock_zt_pool_zbgc_em_service import StockZtPoolZbgcEmService
    service = StockZtPoolZbgcEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zt_pool_zbgc_em/refresh")
async def refresh_stock_zt_pool_zbgc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新炸板股池数据"""
    from app.services.stock.stock_zt_pool_zbgc_em_service import StockZtPoolZbgcEmService
    service = StockZtPoolZbgcEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zt_pool_zbgc_em/clear")
async def clear_stock_zt_pool_zbgc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空炸板股池数据"""
    from app.services.stock.stock_zt_pool_zbgc_em_service import StockZtPoolZbgcEmService
    service = StockZtPoolZbgcEmService(db)
    return await service.clear_data()



# 主营构成-东财 - stock_zygc_em
@router.get("/collections/stock_zygc_em")
async def get_stock_zygc_em(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营构成-东财数据"""
    from app.services.stock.stock_zygc_em_service import StockZygcEmService
    service = StockZygcEmService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zygc_em/overview")
async def get_stock_zygc_em_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营构成-东财数据概览"""
    from app.services.stock.stock_zygc_em_service import StockZygcEmService
    service = StockZygcEmService(db)
    return await service.get_overview()


@router.post("/collections/stock_zygc_em/refresh")
async def refresh_stock_zygc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主营构成-东财数据"""
    from app.services.stock.stock_zygc_em_service import StockZygcEmService
    service = StockZygcEmService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zygc_em/clear")
async def clear_stock_zygc_em(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主营构成-东财数据"""
    from app.services.stock.stock_zygc_em_service import StockZygcEmService
    service = StockZygcEmService(db)
    return await service.clear_data()



# 主营介绍-同花顺 - stock_zyjs_ths
@router.get("/collections/stock_zyjs_ths")
async def get_stock_zyjs_ths(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_zyjs_ths/overview")
async def get_stock_zyjs_ths_overview(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取主营介绍-同花顺数据概览"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.get_overview()


@router.post("/collections/stock_zyjs_ths/refresh")
async def refresh_stock_zyjs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """刷新主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_zyjs_ths/clear")
async def clear_stock_zyjs_ths(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """清空主营介绍-同花顺数据"""
    from app.services.stock.stock_zyjs_ths_service import StockZyjsThsService
    service = StockZyjsThsService(db)
    return await service.clear_data()
