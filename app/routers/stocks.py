"""
股票详情相关API
- 统一响应包: {success, data, message, timestamp}
- 所有端点均需鉴权 (Bearer Token)
- 路径前缀在 main.py 中挂载为 /api，当前路由自身前缀为 /stocks
"""
from typing import Optional, Dict, Any, List, Tuple
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks, UploadFile, File, Body
import logging
import re
import uuid
import asyncio

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.core.response import ok
from app.services.stock_refresh_service import StockRefreshService
from app.services.stock_data_service import StockDataService
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stocks", tags=["stocks"])


def _zfill_code(code: str) -> str:
    try:
        s = str(code).strip()
        if len(s) == 6 and s.isdigit():
            return s
        return s.zfill(6)
    except Exception:
        return str(code)


def _detect_market_and_code(code: str) -> Tuple[str, str]:
    """
    检测股票代码的市场类型并标准化代码

    Args:
        code: 股票代码

    Returns:
        (market, normalized_code): 市场类型和标准化后的代码
            - CN: A股（6位数字）
            - HK: 港股（4-5位数字或带.HK后缀）
            - US: 美股（字母代码）
    """
    code = code.strip().upper()

    # 港股：带.HK后缀
    if code.endswith('.HK'):
        return ('HK', code[:-3].zfill(5))  # 移除.HK，补齐到5位

    # 美股：纯字母
    if re.match(r'^[A-Z]+$', code):
        return ('US', code)

    # 港股：4-5位数字
    if re.match(r'^\d{4,5}$', code):
        return ('HK', code.zfill(5))  # 补齐到5位

    # A股：6位数字
    if re.match(r'^\d{6}$', code):
        return ('CN', code)

    # 默认当作A股处理
    return ('CN', _zfill_code(code))


@router.get("/{code}/quote", response_model=dict)
async def get_quote(
    code: str,
    force_refresh: bool = Query(False, description="是否强制刷新（跳过缓存）"),
    current_user: dict = Depends(get_current_user)
):
    """
    获取股票实时行情（支持A股/港股/美股）

    自动识别市场类型：
    - 6位数字 → A股
    - 4位数字或.HK → 港股
    - 纯字母 → 美股

    参数：
    - code: 股票代码
    - force_refresh: 是否强制刷新（跳过缓存）

    返回字段（data内，蛇形命名）:
      - code, name, market
      - price(close), change_percent(pct_chg), amount, prev_close(估算)
      - turnover_rate, amplitude（振幅，替代量比）
      - trade_date, updated_at
    """
    # 检测市场类型
    market, normalized_code = _detect_market_and_code(code)

    # 港股和美股：使用新服务
    if market in ['HK', 'US']:
        from app.services.stock.stock_quote_service import StockQuoteService
        service = StockQuoteService()
        data = await service.get_quote(code, force_refresh=force_refresh)
        if data:
            return ok(data)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到股票数据")

    db = get_mongo_db()
    stock_collection = db["stock_basic_info"]
    quote_collection = db["market_quotes"]

    # 查询基本股票信息
    stock_doc = await stock_collection.find_one(
        {"code": normalized_code},
        {"name": 1, "market": 1, "industry": 1}
    )
    if not stock_doc:
        logger.warning(f"股票基础信息不存在: {normalized_code}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="股票不存在")

    # 查询最新行情
    quote_doc = await quote_collection.find_one(
        {"code": normalized_code},
        {"_id": 0, "close": 1, "pct_chg": 1, "volume": 1, "amount": 1, "trade_date": 1, "updated_at": 1}
    )
    if not quote_doc:
        logger.warning(f"股票行情数据不存在: {normalized_code}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="无行情数据")

    # 合并数据
    result = {
        "code": normalized_code,
        "name": stock_doc.get("name"),
        "market": stock_doc.get("market", "CN"),
        "price": quote_doc.get("close"),
        "pct_chg": quote_doc.get("pct_chg"),
        "volume": quote_doc.get("volume"),
        "amount": quote_doc.get("amount"),
        "trade_date": quote_doc.get("trade_date"),
        "updated_at": quote_doc.get("updated_at"),
        "industry": stock_doc.get("industry", "")
    }

    return ok(result)


@router.get("/collections")
async def list_stock_collections(
    current_user: dict = Depends(get_current_user),
):
    """获取所有股票相关数据集合列表及其说明"""
    collections = [
        {
            "name": "stock_basic_info",
            "display_name": "股票基础信息",
            "description": "涵盖A股、港股、美股等股票的基础信息，包含代码、名称、行业、市场、总市值、流通市值等核心要素",
            "route": "/stocks/collections/stock_basic_info",
            "fields": ["code", "name", "industry", "market", "list_date", "total_mv", "circ_mv", "pe", "pb"],
            "source": "akshare",
            "category": "基础数据",
            "update_frequency": "每日"
        },
        {
            "name": "market_quotes",
            "display_name": "实时行情数据",
            "description": "涵盖A股、港股、美股等市场的实时行情数据，包括最新价、涨跌幅、成交量、成交额等关键指标",
            "route": "/stocks/collections/market_quotes",
            "fields": ["code", "trade_date", "open", "high", "low", "close", "volume", "amount", "pct_chg", "turnover_rate"],
            "source": "akshare",
            "category": "行情数据",
            "update_frequency": "实时"
        },
        {
            "name": "stock_financial_data",
            "display_name": "财务数据",
            "description": "上市公司财务数据，包括营业收入、净利润、ROE、负债率、每股收益等财务指标",
            "route": "/stocks/collections/stock_financial_data",
            "fields": ["code", "report_period", "revenue", "net_profit", "roe", "debt_to_assets", "eps"],
            "source": "akshare",
            "category": "财务数据",
            "update_frequency": "季度"
        },
        {
            "name": "stock_daily",
            "display_name": "日线行情",
            "description": "股票的日线历史行情数据，包括开盘价、最高价、最低价、收盘价、成交量等完整K线数据",
            "route": "/stocks/collections/stock_daily",
            "fields": ["code", "trade_date", "open", "high", "low", "close", "volume", "amount"],
            "source": "akshare",
            "category": "行情数据",
            "update_frequency": "每日"
        },
        {
            "name": "stock_weekly",
            "display_name": "周线行情",
            "description": "股票的周线历史行情数据，适用于中长期投资分析",
            "route": "/stocks/collections/stock_weekly",
            "fields": ["code", "trade_date", "open", "high", "low", "close", "volume", "amount"],
            "source": "akshare",
            "category": "行情数据",
            "update_frequency": "每周"
        },
        {
            "name": "stock_monthly",
            "display_name": "月线行情",
            "description": "股票的月线历史行情数据，适用于长期趋势分析",
            "route": "/stocks/collections/stock_monthly",
            "fields": ["code", "trade_date", "open", "high", "low", "close", "volume", "amount"],
            "source": "akshare",
            "category": "行情数据",
            "update_frequency": "每月"
        },
        {
            "name": "stock_sgt_reference_exchange_rate_szse",
            "display_name": "深港通参考汇率",
            "description": "深港通-港股通业务的参考汇率信息，包含买入价、卖出价等",
            "route": "/stocks/collections/stock_sgt_reference_exchange_rate_szse",
            "fields": ["适用日期", "参考汇率买入价", "参考汇率卖出价", "货币种类"],
            "source": "东方财富",
            "category": "互联互通",
            "update_frequency": "每日"
        },
        {
            "name": "stock_sgt_reference_exchange_rate_sse",
            "display_name": "沪港通参考汇率",
            "description": "沪港通-港股通信息披露的参考汇率，为跨境投资提供汇率参考",
            "route": "/stocks/collections/stock_sgt_reference_exchange_rate_sse",
            "fields": ["适用日期", "参考汇率买入价", "参考汇率卖出价", "货币种类"],
            "source": "东方财富",
            "category": "互联互通",
            "update_frequency": "每日"
        },
        {
            "name": "stock_hk_ggt_components_em",
            "display_name": "港股通成份股",
            "description": "东方财富网行情中心港股市场港股通成份股的完整股票列表",
            "route": "/stocks/collections/stock_hk_ggt_components_em",
            "fields": ["序号", "代码", "最新价", "涨跌额", "涨跌幅", "今开", "最高", "最低", "昨收", "成交量", "成交额"],
            "source": "东方财富",
            "category": "港股数据",
            "update_frequency": "每日"
        },
        {
            "name": "stock_hsgt_fund_min_em",
            "display_name": "沪深港通分时数据",
            "description": "东方财富数据中心沪深港通市场概括的分时资金流动数据",
            "route": "/stocks/collections/stock_hsgt_fund_min_em",
            "fields": ["日期", "时间", "沪股通", "深股通", "北向资金", "港股通(沪)", "港股通(深)", "南向资金"],
            "source": "东方财富",
            "category": "资金流向",
            "update_frequency": "分时"
        },
        {
            "name": "stock_hsgt_board_rank_em",
            "display_name": "板块排行",
            "description": "东方财富网-数据中心-沪深港通持股-板块排行",
            "route": "/stocks/collections/stock_hsgt_board_rank_em",
            "fields": ["序号", "最新涨跌幅", "报告时间"],
        },
        {
            "name": "stock_hsgt_hold_stock_em",
            "display_name": "个股排行",
            "description": "东方财富网-数据中心-沪深港通持股-个股排行",
            "route": "/stocks/collections/stock_hsgt_hold_stock_em",
            "fields": ["序号", "代码", "今日收盘价", "今日涨跌幅", "日期"],
        },
        {
            "name": "stock_hsgt_stock_statistics_em",
            "display_name": "每日个股统计",
            "description": "东方财富网-数据中心-沪深港通持股-每日个股统计",
            "route": "/stocks/collections/stock_hsgt_stock_statistics_em",
            "fields": ["序号", "代码", "名称", "今日收盘价", "今日涨跌幅"],
        },
        {
            "name": "stock_hsgt_institution_statistics_em",
            "display_name": "机构排行",
            "description": "东方财富网-数据中心-沪深港通持股-机构排行",
            "route": "/stocks/collections/stock_hsgt_institution_statistics_em",
            "fields": ["序号", "机构名称", "持股只数", "持股市值"],
        },
        {
            "name": "stock_hsgt_sh_hk_spot_em",
            "display_name": "沪深港通-港股通(沪>港)实时行情",
            "description": "东方财富-数据中心-沪深港通-港股通(沪>港)实时行情",
            "route": "/stocks/collections/stock_hsgt_sh_hk_spot_em",
            "fields": ["序号", "代码", "最新价", "涨跌额", "涨跌幅"],
        },
        {
            "name": "stock_hsgt_hist_em",
            "display_name": "沪深港通历史数据",
            "description": "东方财富-数据中心-沪深港通-港股通(沪>港)-历史数据",
            "route": "/stocks/collections/stock_hsgt_hist_em",
            "fields": ["日期", "当日成交净买额", "买入成交额", "卖出成交额"],
        },
        {
            "name": "stock_hsgt_individual_em",
            "display_name": "沪深港通持股-个股",
            "description": "东方财富-数据中心-沪深港通持股-个股",
            "route": "/stocks/collections/stock_hsgt_individual_em",
            "fields": ["持股日期", "当日收盘价", "持股数量", "持股市值"],
        },
        {
            "name": "stock_hsgt_individual_detail_em",
            "display_name": "个股详情",
            "description": "东方财富-数据中心-沪深港通持股-个股详情",
            "route": "/stocks/collections/stock_hsgt_individual_detail_em",
            "fields": ["日期", "收盘价", "涨跌幅", "持股量", "占流通股比"],
        },
        {
            "name": "stock_em_hsgt_north_net_flow_in",
            "display_name": "北向资金流入",
            "description": "东方财富-数据中心-沪深港通-北向资金流入",
            "route": "/stocks/collections/stock_em_hsgt_north_net_flow_in",
            "fields": ["日期", "沪股通", "深股通", "北向资金"],
        },
        {
            "name": "stock_em_hsgt_south_net_flow_in",
            "display_name": "南向资金流入",
            "description": "东方财富-数据中心-沪深港通-南向资金流入",
            "route": "/stocks/collections/stock_em_hsgt_south_net_flow_in",
            "fields": ["日期", "港股通(沪)", "港股通(深)", "南向资金"],
        },
        {
            "name": "stock_em_hsgt_hold_stock",
            "display_name": "历史持股统计",
            "description": "东方财富-数据中心-沪深港通-历史持股统计",
            "route": "/stocks/collections/stock_em_hsgt_hold_stock",
            "fields": ["日期", "个股", "持股数量", "持股市值"],
        },
        {
            "name": "stock_tfp_em",
            "display_name": "股票停复牌信息",
            "description": "东方财富数据中心特色数据的股票停复牌信息",
            "route": "/stocks/collections/stock_tfp_em",
            "fields": ["代码", "名称", "停牌时间", "预计复牌时间"],
            "source": "东方财富",
            "category": "公告数据",
            "update_frequency": "实时"
        },
        {
            "name": "stock_zh_a_new",
            "display_name": "新股数据",
            "description": "东方财富-数据中心-新股数据",
            "route": "/stocks/collections/stock_zh_a_new",
            "fields": ["代码", "名称", "发行价", "申购日期"],
        },
        {
            "name": "stock_ipo_info",
            "display_name": "新股申购信息",
            "description": "新浪财经-新股申购信息",
            "route": "/stocks/collections/stock_ipo_info",
            "fields": ["代码", "名称", "申购日期", "发行价"],
        },
        {
            "name": "stock_xgsglb_em",
            "display_name": "新股申购概览",
            "description": "东方财富-数据中心-新股数据-新股申购与中签查询-申购概览",
            "route": "/stocks/collections/stock_xgsglb_em",
            "fields": ["序号", "代码", "名称", "申购日期"],
        },
        {
            "name": "stock_dzjy_sctj",
            "display_name": "大宗交易-市场统计",
            "description": "东方财富-数据中心-特色数据-大宗交易-市场统计",
            "route": "/stocks/collections/stock_dzjy_sctj",
            "fields": ["日期", "成交总额", "成交总量", "成交笔数"],
        },
        {
            "name": "stock_dzjy_mrmx",
            "display_name": "大宗交易-每日明细",
            "description": "东方财富-数据中心-特色数据-大宗交易-每日明细",
            "route": "/stocks/collections/stock_dzjy_mrmx",
            "fields": ["代码", "名称", "成交价", "成交量"],
        },
        {
            "name": "stock_dzjy_mrtj",
            "display_name": "大宗交易-每日统计",
            "description": "东方财富-数据中心-特色数据-大宗交易-每日统计",
            "route": "/stocks/collections/stock_dzjy_mrtj",
            "fields": ["代码", "名称", "成交总量", "成交总额"],
        },
        {
            "name": "stock_jgdy_tj_em",
            "display_name": "机构调研统计",
            "description": "东方财富-数据中心-特色数据-机构调研统计",
            "route": "/stocks/collections/stock_jgdy_tj_em",
            "fields": ["日期", "调研机构数量", "调研公司数量"],
        },
        {
            "name": "stock_jgdy_detail_em",
            "display_name": "机构调研明细",
            "description": "东方财富-数据中心-特色数据-机构调研-明细",
            "route": "/stocks/collections/stock_jgdy_detail_em",
            "fields": ["代码", "名称", "调研日期", "接待机构数量"],
        },
        {
            "name": "stock_jgcyd_em",
            "display_name": "机构持仓地图",
            "description": "东方财富-数据中心-特色数据-机构持仓地图",
            "route": "/stocks/collections/stock_jgcyd_em",
            "fields": ["代码", "名称", "持仓数量", "持仓市值"],
        },
        {
            "name": "stock_gpzy_profile_em",
            "display_name": "个股资讯-东财",
            "description": "东方财富-数据中心-特色数据-个股资讯",
            "route": "/stocks/collections/stock_gpzy_profile_em",
            "fields": ["代码", "名称", "最新价", "涨跌幅"],
        },
        {
            "name": "stock_news_em",
            "display_name": "个股新闻-东财",
            "description": "东方财富-个股新闻",
            "route": "/stocks/collections/stock_news_em",
            "fields": ["标题", "发布时间", "来源"],
        },
        {
            "name": "stock_js_weibo_nlp_time",
            "display_name": "个股新闻-微博",
            "description": "微博财经-个股新闻",
            "route": "/stocks/collections/stock_js_weibo_nlp_time",
            "fields": ["时间", "内容", "情绪"],
        },
        {
            "name": "stock_cjrl_em",
            "display_name": "财经日历",
            "description": "东方财富-数据中心-特色数据-财经日历",
            "route": "/stocks/collections/stock_cjrl_em",
            "fields": ["日期", "内容"],
        },
        {
            "name": "stock_yjfp_em",
            "display_name": "业绩报表-业绩快报",
            "description": "东方财富-数据中心-年报季报-业绩快报",
            "route": "/stocks/collections/stock_yjfp_em",
            "fields": ["代码", "名称", "报告期"],
        },
        {
            "name": "stock_yjyg_em",
            "display_name": "业绩报表-业绩预告",
            "description": "东方财富-数据中心-年报季报-业绩预告",
            "route": "/stocks/collections/stock_yjyg_em",
            "fields": ["代码", "名称", "报告期"],
        },
        {
            "name": "stock_yysj_em",
            "display_name": "业绩报表-预约披露",
            "description": "东方财富-数据中心-年报季报-预约披露",
            "route": "/stocks/collections/stock_yysj_em",
            "fields": ["代码", "名称", "首次预约时间"],
        },
        {
            "name": "stock_add_stock_cninfo",
            "display_name": "增发-巨潮资讯",
            "description": "增发-巨潮资讯",
            "route": "/stocks/collections/stock_add_stock_cninfo",
            "fields": ["代码"],
        },
        {
            "name": "stock_restricted_release_queue_em",
            "display_name": "限售解禁-东财",
            "description": "限售解禁-东财",
            "route": "/stocks/collections/stock_restricted_release_queue_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_info_change_name_em",
            "display_name": "信息变更-公司更名",
            "description": "信息变更-公司更名",
            "route": "/stocks/collections/stock_info_change_name_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_board_industry_name_em",
            "display_name": "行业分类",
            "description": "行业分类",
            "route": "/stocks/collections/stock_board_industry_name_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_gpgk_em",
            "display_name": "股本变动",
            "description": "股本变动",
            "route": "/stocks/collections/stock_gpgk_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_fhps_detail_ths",
            "display_name": "分红情况-同花顺",
            "description": "分红情况-同花顺",
            "route": "/stocks/collections/stock_fhps_detail_ths",
            "fields": ["代码"],
        },
        {
            "name": "stock_hk_fhpx_detail_ths",
            "display_name": "分红配送详情-港股-同花顺",
            "description": "分红配送详情-港股-同花顺",
            "route": "/stocks/collections/stock_hk_fhpx_detail_ths",
            "fields": ["代码"],
        },
        {
            "name": "stock_fund_flow_individual",
            "display_name": "个股资金流",
            "description": "个股资金流",
            "route": "/stocks/collections/stock_fund_flow_individual",
            "fields": ["代码"],
        },
        {
            "name": "stock_fund_flow_concept",
            "display_name": "概念资金流",
            "description": "概念资金流",
            "route": "/stocks/collections/stock_fund_flow_concept",
            "fields": ["代码"],
        },
        {
            "name": "stock_fund_flow_industry",
            "display_name": "行业资金流",
            "description": "行业资金流",
            "route": "/stocks/collections/stock_fund_flow_industry",
            "fields": ["代码"],
        },
        {
            "name": "stock_fund_flow_big_deal",
            "display_name": "大单追踪",
            "description": "大单追踪",
            "route": "/stocks/collections/stock_fund_flow_big_deal",
            "fields": ["代码"],
        },
        {
            "name": "stock_individual_fund_flow",
            "display_name": "个股资金流",
            "description": "个股资金流",
            "route": "/stocks/collections/stock_individual_fund_flow",
            "fields": ["代码"],
        },
        {
            "name": "stock_individual_fund_flow_rank",
            "display_name": "个股资金流排名",
            "description": "个股资金流排名",
            "route": "/stocks/collections/stock_individual_fund_flow_rank",
            "fields": ["代码"],
        },
        {
            "name": "stock_market_fund_flow",
            "display_name": "大盘资金流",
            "description": "大盘资金流",
            "route": "/stocks/collections/stock_market_fund_flow",
            "fields": ["代码"],
        },
        {
            "name": "stock_sector_fund_flow_rank",
            "display_name": "板块资金流排名",
            "description": "板块资金流排名",
            "route": "/stocks/collections/stock_sector_fund_flow_rank",
            "fields": ["代码"],
        },
        {
            "name": "stock_main_fund_flow",
            "display_name": "主力净流入排名",
            "description": "主力净流入排名",
            "route": "/stocks/collections/stock_main_fund_flow",
            "fields": ["代码"],
        },
        {
            "name": "stock_sector_fund_flow_summary",
            "display_name": "行业个股资金流",
            "description": "行业个股资金流",
            "route": "/stocks/collections/stock_sector_fund_flow_summary",
            "fields": ["代码"],
        },
        {
            "name": "stock_sector_fund_flow_hist",
            "display_name": "行业历史资金流",
            "description": "行业历史资金流",
            "route": "/stocks/collections/stock_sector_fund_flow_hist",
            "fields": ["代码"],
        },
        {
            "name": "stock_concept_fund_flow_hist",
            "display_name": "概念历史资金流",
            "description": "概念历史资金流",
            "route": "/stocks/collections/stock_concept_fund_flow_hist",
            "fields": ["代码"],
        },
        {
            "name": "stock_cyq_em",
            "display_name": "筹码分布",
            "description": "筹码分布",
            "route": "/stocks/collections/stock_cyq_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_gddh_em",
            "display_name": "股东大会",
            "description": "股东大会",
            "route": "/stocks/collections/stock_gddh_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_zdhtmx_em",
            "display_name": "重大合同",
            "description": "重大合同",
            "route": "/stocks/collections/stock_zdhtmx_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_research_report_em",
            "display_name": "个股研报",
            "description": "个股研报",
            "route": "/stocks/collections/stock_research_report_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_notice_report",
            "display_name": "沪深京A股公告",
            "description": "沪深京A股公告",
            "route": "/stocks/collections/stock_notice_report",
            "fields": ["代码"],
        },
        {
            "name": "stock_financial_report_sina",
            "display_name": "财务报表-新浪",
            "description": "财务报表-新浪",
            "route": "/stocks/collections/stock_financial_report_sina",
            "fields": ["代码"],
        },
        {
            "name": "stock_balance_sheet_by_report_em",
            "display_name": "资产负债表-按报告期",
            "description": "资产负债表-按报告期",
            "route": "/stocks/collections/stock_balance_sheet_by_report_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_profit_sheet_by_quarterly_em",
            "display_name": "利润表-按单季度",
            "description": "利润表-按单季度",
            "route": "/stocks/collections/stock_profit_sheet_by_quarterly_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_cash_flow_sheet_by_report_em",
            "display_name": "现金流量表-按报告期",
            "description": "现金流量表-按报告期",
            "route": "/stocks/collections/stock_cash_flow_sheet_by_report_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_cash_flow_sheet_by_yearly_em",
            "display_name": "现金流量表-按年度",
            "description": "现金流量表-按年度",
            "route": "/stocks/collections/stock_cash_flow_sheet_by_yearly_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_cash_flow_sheet_by_quarterly_em",
            "display_name": "现金流量表-按单季度",
            "description": "现金流量表-按单季度",
            "route": "/stocks/collections/stock_cash_flow_sheet_by_quarterly_em",
            "fields": ["代码"],
        },
        {
            "name": "stock_financial_debt_ths",
            "display_name": "资产负债表",
            "description": "资产负债表",
            "route": "/stocks/collections/stock_financial_debt_ths",
            "fields": ["代码"],
        },
        {
            "name": "stock_financial_benefit_ths",
            "display_name": "利润表",
            "description": "利润表",
            "route": "/stocks/collections/stock_financial_benefit_ths",
            "fields": ["代码"],
        },
        {
            "name": "stock_financial_cash_ths",
            "display_name": "现金流量表",
            "description": "现金流量表",
            "route": "/stocks/collections/stock_financial_cash_ths",
            "fields": ["code"],
        },
        {
            "name": "stock_balance_sheet_by_report_delisted_em",
            "display_name": "资产负债表-按报告期",
            "description": "资产负债表-按报告期",
            "route": "/stocks/collections/stock_balance_sheet_by_report_delisted_em",
            "fields": ["code"],
        },
        {
            "name": "stock_profit_sheet_by_report_delisted_em",
            "display_name": "利润表-按报告期",
            "description": "利润表-按报告期",
            "route": "/stocks/collections/stock_profit_sheet_by_report_delisted_em",
            "fields": ["code"],
        },
        {
            "name": "stock_cash_flow_sheet_by_report_delisted_em",
            "display_name": "现金流量表-按报告期",
            "description": "现金流量表-按报告期",
            "route": "/stocks/collections/stock_cash_flow_sheet_by_report_delisted_em",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_hk_report_em",
            "display_name": "港股财务报表",
            "description": "港股财务报表",
            "route": "/stocks/collections/stock_financial_hk_report_em",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_us_report_em",
            "display_name": "美股财务报表",
            "description": "美股财务报表",
            "route": "/stocks/collections/stock_financial_us_report_em",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_abstract",
            "display_name": "关键指标-新浪",
            "description": "新浪财经的关键财务指标数据",
            "route": "/stocks/collections/stock_financial_abstract",
            "fields": ["code"],
            "source": "新浪财经",
            "category": "财务数据",
            "update_frequency": "季度"
        },
        {
            "name": "stock_financial_abstract_ths",
            "display_name": "关键指标-同花顺",
            "description": "关键指标-同花顺",
            "route": "/stocks/collections/stock_financial_abstract_ths",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_analysis_indicator_em",
            "display_name": "主要指标-东方财富",
            "description": "主要指标-东方财富",
            "route": "/stocks/collections/stock_financial_analysis_indicator_em",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_analysis_indicator",
            "display_name": "财务指标",
            "description": "财务指标",
            "route": "/stocks/collections/stock_financial_analysis_indicator",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_hk_analysis_indicator_em",
            "display_name": "港股财务指标",
            "description": "港股财务指标",
            "route": "/stocks/collections/stock_financial_hk_analysis_indicator_em",
            "fields": ["code"],
        },
        {
            "name": "stock_financial_us_analysis_indicator_em",
            "display_name": "美股财务指标",
            "description": "美股财务指标",
            "route": "/stocks/collections/stock_financial_us_analysis_indicator_em",
            "fields": ["code"],
        },
        {
            "name": "stock_history_dividend",
            "display_name": "历史分红",
            "description": "历史分红",
            "route": "/stocks/collections/stock_history_dividend",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_free_top_10_em",
            "display_name": "十大流通股东(个股)",
            "description": "十大流通股东(个股)",
            "route": "/stocks/collections/stock_gdfx_free_top_10_em",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_top_10_em",
            "display_name": "十大股东(个股)",
            "description": "十大股东(个股)",
            "route": "/stocks/collections/stock_gdfx_top_10_em",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_free_holding_change_em",
            "display_name": "股东持股变动统计-十大流通股东",
            "description": "股东持股变动统计-十大流通股东",
            "route": "/stocks/collections/stock_gdfx_free_holding_change_em",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_holding_change_em",
            "display_name": "股东持股变动统计-十大股东",
            "description": "股东持股变动统计-十大股东",
            "route": "/stocks/collections/stock_gdfx_holding_change_em",
            "fields": ["code"],
        },
        {
            "name": "stock_management_change_ths",
            "display_name": "高管持股变动统计",
            "description": "高管持股变动统计",
            "route": "/stocks/collections/stock_management_change_ths",
            "fields": ["code"],
        },
        {
            "name": "stock_shareholder_change_ths",
            "display_name": "股东持股变动统计",
            "description": "股东持股变动统计",
            "route": "/stocks/collections/stock_shareholder_change_ths",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_free_holding_analyse_em",
            "display_name": "股东持股分析-十大流通股东",
            "description": "股东持股分析-十大流通股东",
            "route": "/stocks/collections/stock_gdfx_free_holding_analyse_em",
            "fields": ["code"],
        },
        {
            "name": "stock_gdfx_holding_analyse_em",
            "display_name": "股东持股分析-十大股东",
            "description": "股东持股分析-十大股东",
            "route": "/stocks/collections/stock_gdfx_holding_analyse_em",
            "fields": ["code"],
        },
{
    "name": "news_report_time_baidu",
    "display_name": "财报发行-百度",
    "description": "百度财经的财报发行数据",
    "route": "/stocks/collections/news_report_time_baidu",
    "fields": [],
    "source": "百度财经",
    "category": "公告数据",
    "update_frequency": "实时"
},
{
    "name": "news_trade_notify_dividend_baidu",
    "display_name": "分红派息-百度",
    "description": "百度财经的分红派息数据",
    "route": "/stocks/collections/news_trade_notify_dividend_baidu",
    "fields": [],
    "source": "百度财经",
    "category": "公告数据",
    "update_frequency": "实时"
},
{
    "name": "news_trade_notify_suspend_baidu",
    "display_name": "停复牌-百度",
    "description": "百度财经的停复牌数据",
    "route": "/stocks/collections/news_trade_notify_suspend_baidu",
    "fields": [],
    "source": "百度财经",
    "category": "公告数据",
    "update_frequency": "实时"
},
{
    "name": "stock_a_all_pb",
    "display_name": "A股等权重与中位数市净率",
    "description": "A股整体市场的等权重与中位数市净率数据",
    "route": "/stocks/collections/stock_a_all_pb",
    "fields": [],
    "source": "乐咕乐股",
    "category": "估值指标",
    "update_frequency": "每日"
},
{
    "name": "stock_a_below_net_asset_statistics",
    "display_name": "破净股统计",
    "description": "A股市场破净股（市净率小于1）的统计数据分析",
    "route": "/stocks/collections/stock_a_below_net_asset_statistics",
    "fields": [],
    "source": "乐咕乐股",
    "category": "估值指标",
    "update_frequency": "每日"
},
{
    "name": "stock_a_congestion_lg",
    "display_name": "大盘拥挤度",
    "description": "A股大盘市场拥挤度指标数据",
    "route": "/stocks/collections/stock_a_congestion_lg",
    "fields": [],
    "source": "乐咕乐股",
    "category": "情绪指标",
    "update_frequency": "每日"
},
{
    "name": "stock_a_gxl_lg",
    "display_name": "A股股息率",
    "description": "A股整体市场股息率数据",
    "route": "/stocks/collections/stock_a_gxl_lg",
    "fields": [],
    "source": "乐咕乐股",
    "category": "估值指标",
    "update_frequency": "每日"
},
{
    "name": "stock_a_high_low_statistics",
    "display_name": "创新高和新低股票数量统计",
    "description": "A股市场创新高和创新低股票数量的统计数据分析",
    "route": "/stocks/collections/stock_a_high_low_statistics",
    "fields": [],
    "source": "乐咕乐股",
    "category": "市场统计",
    "update_frequency": "每日"
},
{
    "name": "stock_a_ttm_lyr",
    "display_name": "A股等权重与中位数市盈率",
    "description": "A股整体市场的等权重与中位数滚动市盈率数据",
    "route": "/stocks/collections/stock_a_ttm_lyr",
    "fields": [],
    "source": "乐咕乐股",
    "category": "估值指标",
    "update_frequency": "每日"
},
{
    "name": "stock_account_statistics_em",
    "display_name": "股票账户统计月度",
    "description": "东方财富的月度股票账户统计数据",
    "route": "/stocks/collections/stock_account_statistics_em",
    "fields": [],
    "source": "东方财富",
    "category": "市场统计",
    "update_frequency": "每月"
},
{
    "name": "stock_add_stock",
    "display_name": "股票增发",
    "description": "股票增发相关数据",
    "route": "/stocks/collections/stock_add_stock",
    "fields": [],
    "source": "akshare",
    "category": "公告数据",
    "update_frequency": "实时"
},
{
    "name": "stock_allotment_cninfo",
    "display_name": "配股实施方案-巨潮资讯",
    "description": "巨潮资讯的配股实施方案数据",
    "route": "/stocks/collections/stock_allotment_cninfo",
    "fields": [],
    "source": "巨潮资讯",
    "category": "公告数据",
    "update_frequency": "实时"
},
{
    "name": "stock_analyst_detail_em",
    "display_name": "分析师详情",
    "description": "分析师详情数据",
    "route": "/stocks/collections/stock_analyst_detail_em",
    "fields": [],
},
{
    "name": "stock_analyst_rank_em",
    "display_name": "分析师指数排行",
    "description": "分析师指数排行数据",
    "route": "/stocks/collections/stock_analyst_rank_em",
    "fields": [],
},
{
    "name": "stock_balance_sheet_by_yearly_em",
    "display_name": "资产负债表-按年度",
    "description": "资产负债表-按年度数据",
    "route": "/stocks/collections/stock_balance_sheet_by_yearly_em",
    "fields": [],
},
{
    "name": "stock_bid_ask_em",
    "display_name": "行情报价",
    "description": "行情报价数据",
    "route": "/stocks/collections/stock_bid_ask_em",
    "fields": [],
},
{
    "name": "stock_bj_a_spot_em",
    "display_name": "京 A 股",
    "description": "京 A 股数据",
    "route": "/stocks/collections/stock_bj_a_spot_em",
    "fields": [],
},
{
    "name": "stock_board_change_em",
    "display_name": "板块异动详情",
    "description": "板块异动详情数据",
    "route": "/stocks/collections/stock_board_change_em",
    "fields": [],
},
{
    "name": "stock_board_concept_cons_em",
    "display_name": "东方财富-成份股",
    "description": "东方财富-成份股数据",
    "route": "/stocks/collections/stock_board_concept_cons_em",
    "fields": [],
},
{
    "name": "stock_board_concept_hist_em",
    "display_name": "东方财富-指数",
    "description": "东方财富-指数数据",
    "route": "/stocks/collections/stock_board_concept_hist_em",
    "fields": [],
},
{
    "name": "stock_board_concept_hist_min_em",
    "display_name": "东方财富-指数-分时",
    "description": "东方财富-指数-分时数据",
    "route": "/stocks/collections/stock_board_concept_hist_min_em",
    "fields": [],
},
{
    "name": "stock_board_concept_index_ths",
    "display_name": "同花顺-概念板块指数",
    "description": "同花顺-概念板块指数数据",
    "route": "/stocks/collections/stock_board_concept_index_ths",
    "fields": [],
},
{
    "name": "stock_board_concept_info_ths",
    "display_name": "同花顺-概念板块简介",
    "description": "同花顺-概念板块简介数据",
    "route": "/stocks/collections/stock_board_concept_info_ths",
    "fields": [],
},
{
    "name": "stock_board_concept_name_em",
    "display_name": "东方财富-概念板块",
    "description": "东方财富-概念板块数据",
    "route": "/stocks/collections/stock_board_concept_name_em",
    "fields": [],
},
{
    "name": "stock_board_concept_spot_em",
    "display_name": "东方财富-概念板块-实时行情",
    "description": "东方财富-概念板块-实时行情数据",
    "route": "/stocks/collections/stock_board_concept_spot_em",
    "fields": [],
},
{
    "name": "stock_board_industry_cons_em",
    "display_name": "东方财富-成份股",
    "description": "东方财富-成份股数据",
    "route": "/stocks/collections/stock_board_industry_cons_em",
    "fields": [],
},
{
    "name": "stock_board_industry_hist_em",
    "display_name": "东方财富-指数-日频",
    "description": "东方财富-指数-日频数据",
    "route": "/stocks/collections/stock_board_industry_hist_em",
    "fields": [],
},
{
    "name": "stock_board_industry_hist_min_em",
    "display_name": "东方财富-指数-分时",
    "description": "东方财富-指数-分时数据",
    "route": "/stocks/collections/stock_board_industry_hist_min_em",
    "fields": [],
},
{
    "name": "stock_board_industry_index_ths",
    "display_name": "同花顺-指数",
    "description": "同花顺-指数数据",
    "route": "/stocks/collections/stock_board_industry_index_ths",
    "fields": [],
},
{
    "name": "stock_board_industry_spot_em",
    "display_name": "东方财富-行业板块-实时行情",
    "description": "东方财富-行业板块-实时行情数据",
    "route": "/stocks/collections/stock_board_industry_spot_em",
    "fields": [],
},
{
    "name": "stock_board_industry_summary_ths",
    "display_name": "同花顺-同花顺行业一览表",
    "description": "同花顺-同花顺行业一览表数据",
    "route": "/stocks/collections/stock_board_industry_summary_ths",
    "fields": [],
},
{
    "name": "stock_buffett_index_lg",
    "display_name": "巴菲特指标",
    "description": "巴菲特指标数据",
    "route": "/stocks/collections/stock_buffett_index_lg",
    "fields": [],
},
{
    "name": "stock_cg_equity_mortgage_cninfo",
    "display_name": "股权质押",
    "description": "股权质押数据",
    "route": "/stocks/collections/stock_cg_equity_mortgage_cninfo",
    "fields": [],
},
{
    "name": "stock_cg_guarantee_cninfo",
    "display_name": "对外担保",
    "description": "对外担保数据",
    "route": "/stocks/collections/stock_cg_guarantee_cninfo",
    "fields": [],
},
{
    "name": "stock_cg_lawsuit_cninfo",
    "display_name": "公司诉讼",
    "description": "公司诉讼数据",
    "route": "/stocks/collections/stock_cg_lawsuit_cninfo",
    "fields": [],
},
{
    "name": "stock_changes_em",
    "display_name": "盘口异动",
    "description": "盘口异动数据",
    "route": "/stocks/collections/stock_changes_em",
    "fields": [],
},
{
    "name": "stock_circulate_stock_holder",
    "display_name": "流通股东",
    "description": "流通股东数据",
    "route": "/stocks/collections/stock_circulate_stock_holder",
    "fields": [],
},
{
    "name": "stock_comment_detail_scrd_desire_daily_em",
    "display_name": "日度市场参与意愿",
    "description": "日度市场参与意愿数据",
    "route": "/stocks/collections/stock_comment_detail_scrd_desire_daily_em",
    "fields": [],
},
{
    "name": "stock_comment_detail_scrd_desire_em",
    "display_name": "市场参与意愿",
    "description": "市场参与意愿数据",
    "route": "/stocks/collections/stock_comment_detail_scrd_desire_em",
    "fields": [],
},
{
    "name": "stock_comment_detail_scrd_focus_em",
    "display_name": "用户关注指数",
    "description": "用户关注指数数据",
    "route": "/stocks/collections/stock_comment_detail_scrd_focus_em",
    "fields": [],
},
{
    "name": "stock_comment_detail_zhpj_lspf_em",
    "display_name": "历史评分",
    "description": "历史评分数据",
    "route": "/stocks/collections/stock_comment_detail_zhpj_lspf_em",
    "fields": [],
},
{
    "name": "stock_comment_detail_zlkp_jgcyd_em",
    "display_name": "机构参与度",
    "description": "机构参与度数据",
    "route": "/stocks/collections/stock_comment_detail_zlkp_jgcyd_em",
    "fields": [],
},
{
    "name": "stock_comment_em",
    "display_name": "千股千评",
    "description": "千股千评数据",
    "route": "/stocks/collections/stock_comment_em",
    "fields": [],
},
{
    "name": "stock_concept_cons_futu",
    "display_name": "富途牛牛-美股概念-成分股",
    "description": "富途牛牛-美股概念-成分股数据",
    "route": "/stocks/collections/stock_concept_cons_futu",
    "fields": [],
},
{
    "name": "stock_cy_a_spot_em",
    "display_name": "创业板",
    "description": "创业板数据",
    "route": "/stocks/collections/stock_cy_a_spot_em",
    "fields": [],
},
{
    "name": "stock_dividend_cninfo",
    "display_name": "历史分红",
    "description": "历史分红数据",
    "route": "/stocks/collections/stock_dividend_cninfo",
    "fields": [],
},
{
    "name": "stock_dxsyl_em",
    "display_name": "打新收益率",
    "description": "打新收益率数据",
    "route": "/stocks/collections/stock_dxsyl_em",
    "fields": [],
},
{
    "name": "stock_dzjy_hygtj",
    "display_name": "活跃 A 股统计",
    "description": "活跃 A 股统计数据",
    "route": "/stocks/collections/stock_dzjy_hygtj",
    "fields": [],
},
{
    "name": "stock_dzjy_hyyybtj",
    "display_name": "活跃营业部统计",
    "description": "活跃营业部统计数据",
    "route": "/stocks/collections/stock_dzjy_hyyybtj",
    "fields": [],
},
{
    "name": "stock_dzjy_yybph",
    "display_name": "营业部排行",
    "description": "营业部排行数据",
    "route": "/stocks/collections/stock_dzjy_yybph",
    "fields": [],
},
{
    "name": "stock_ebs_lg",
    "display_name": "股债利差",
    "description": "股债利差数据",
    "route": "/stocks/collections/stock_ebs_lg",
    "fields": [],
},
{
    "name": "stock_esg_hz_sina",
    "display_name": "华证指数",
    "description": "华证指数数据",
    "route": "/stocks/collections/stock_esg_hz_sina",
    "fields": [],
},
{
    "name": "stock_esg_msci_sina",
    "display_name": "MSCI",
    "description": "MSCI数据",
    "route": "/stocks/collections/stock_esg_msci_sina",
    "fields": [],
},
{
    "name": "stock_esg_rate_sina",
    "display_name": "ESG 评级数据",
    "description": "ESG 评级数据数据",
    "route": "/stocks/collections/stock_esg_rate_sina",
    "fields": [],
},
{
    "name": "stock_esg_rft_sina",
    "display_name": "路孚特",
    "description": "路孚特数据",
    "route": "/stocks/collections/stock_esg_rft_sina",
    "fields": [],
},
{
    "name": "stock_esg_zd_sina",
    "display_name": "秩鼎",
    "description": "秩鼎数据",
    "route": "/stocks/collections/stock_esg_zd_sina",
    "fields": [],
},
{
    "name": "stock_fhps_detail_em",
    "display_name": "分红配送详情-东财",
    "description": "分红配送详情-东财数据",
    "route": "/stocks/collections/stock_fhps_detail_em",
    "fields": [],
},
{
    "name": "stock_fhps_em",
    "display_name": "分红配送-东财",
    "description": "分红配送-东财数据",
    "route": "/stocks/collections/stock_fhps_em",
    "fields": [],
},
{
    "name": "stock_fund_stock_holder",
    "display_name": "基金持股",
    "description": "基金持股数据",
    "route": "/stocks/collections/stock_fund_stock_holder",
    "fields": [],
},
{
    "name": "stock_gdfx_free_holding_detail_em",
    "display_name": "股东持股明细-十大流通股东",
    "description": "股东持股明细-十大流通股东数据",
    "route": "/stocks/collections/stock_gdfx_free_holding_detail_em",
    "fields": [],
},
{
    "name": "stock_gdfx_free_holding_statistics_em",
    "display_name": "股东持股统计-十大流通股东",
    "description": "股东持股统计-十大流通股东数据",
    "route": "/stocks/collections/stock_gdfx_free_holding_statistics_em",
    "fields": [],
},
{
    "name": "stock_gdfx_free_holding_teamwork_em",
    "display_name": "股东协同-十大流通股东",
    "description": "股东协同-十大流通股东数据",
    "route": "/stocks/collections/stock_gdfx_free_holding_teamwork_em",
    "fields": [],
},
{
    "name": "stock_gdfx_holding_detail_em",
    "display_name": "股东持股明细-十大股东",
    "description": "股东持股明细-十大股东数据",
    "route": "/stocks/collections/stock_gdfx_holding_detail_em",
    "fields": [],
},
{
    "name": "stock_gdfx_holding_statistics_em",
    "display_name": "股东持股统计-十大股东",
    "description": "股东持股统计-十大股东数据",
    "route": "/stocks/collections/stock_gdfx_holding_statistics_em",
    "fields": [],
},
{
    "name": "stock_gdfx_holding_teamwork_em",
    "display_name": "股东协同-十大股东",
    "description": "股东协同-十大股东数据",
    "route": "/stocks/collections/stock_gdfx_holding_teamwork_em",
    "fields": [],
},
{
    "name": "stock_ggcg_em",
    "display_name": "股东增减持",
    "description": "股东增减持数据",
    "route": "/stocks/collections/stock_ggcg_em",
    "fields": [],
},
{
    "name": "stock_gpzy_distribute_statistics_bank_em",
    "display_name": "质押机构分布统计-银行",
    "description": "质押机构分布统计-银行数据",
    "route": "/stocks/collections/stock_gpzy_distribute_statistics_bank_em",
    "fields": [],
},
{
    "name": "stock_gpzy_distribute_statistics_company_em",
    "display_name": "质押机构分布统计-证券公司",
    "description": "质押机构分布统计-证券公司数据",
    "route": "/stocks/collections/stock_gpzy_distribute_statistics_company_em",
    "fields": [],
},
{
    "name": "stock_gpzy_industry_data_em",
    "display_name": "上市公司质押比例",
    "description": "上市公司质押比例数据",
    "route": "/stocks/collections/stock_gpzy_industry_data_em",
    "fields": [],
},
{
    "name": "stock_gpzy_pledge_ratio_detail_em",
    "display_name": "重要股东股权质押明细",
    "description": "重要股东股权质押明细数据",
    "route": "/stocks/collections/stock_gpzy_pledge_ratio_detail_em",
    "fields": [],
},
{
    "name": "stock_gpzy_pledge_ratio_em",
    "display_name": "上市公司质押比例",
    "description": "上市公司质押比例数据",
    "route": "/stocks/collections/stock_gpzy_pledge_ratio_em",
    "fields": [],
},
{
    "name": "stock_gsrl_gsdt_em",
    "display_name": "公司动态",
    "description": "公司动态数据",
    "route": "/stocks/collections/stock_gsrl_gsdt_em",
    "fields": [],
},
{
    "name": "stock_history_dividend_detail",
    "display_name": "分红配股",
    "description": "分红配股数据",
    "route": "/stocks/collections/stock_history_dividend_detail",
    "fields": [],
},
{
    "name": "stock_hk_company_profile_em",
    "display_name": "公司资料",
    "description": "公司资料数据",
    "route": "/stocks/collections/stock_hk_company_profile_em",
    "fields": [],
},
{
    "name": "stock_hk_daily",
    "display_name": "历史行情数据-新浪",
    "description": "历史行情数据-新浪数据",
    "route": "/stocks/collections/stock_hk_daily",
    "fields": [],
},
{
    "name": "stock_hk_dividend_payout_em",
    "display_name": "分红派息",
    "description": "分红派息数据",
    "route": "/stocks/collections/stock_hk_dividend_payout_em",
    "fields": [],
},
{
    "name": "stock_hk_famous_spot_em",
    "display_name": "知名港股",
    "description": "知名港股数据",
    "route": "/stocks/collections/stock_hk_famous_spot_em",
    "fields": [],
},
{
    "name": "stock_hk_financial_indicator_em",
    "display_name": "财务指标",
    "description": "财务指标数据",
    "route": "/stocks/collections/stock_hk_financial_indicator_em",
    "fields": [],
},
{
    "name": "stock_hk_growth_comparison_em",
    "display_name": "成长性对比",
    "description": "成长性对比数据",
    "route": "/stocks/collections/stock_hk_growth_comparison_em",
    "fields": [],
},
{
    "name": "stock_hk_gxl_lg",
    "display_name": "恒生指数股息率",
    "description": "恒生指数股息率数据",
    "route": "/stocks/collections/stock_hk_gxl_lg",
    "fields": [],
},
{
    "name": "stock_hk_hist",
    "display_name": "历史行情数据-东财",
    "description": "历史行情数据-东财数据",
    "route": "/stocks/collections/stock_hk_hist",
    "fields": [],
},
{
    "name": "stock_hk_hist_min_em",
    "display_name": "分时数据-东财",
    "description": "分时数据-东财数据",
    "route": "/stocks/collections/stock_hk_hist_min_em",
    "fields": [],
},
{
    "name": "stock_hk_hot_rank_detail_em",
    "display_name": "港股",
    "description": "港股数据",
    "route": "/stocks/collections/stock_hk_hot_rank_detail_em",
    "fields": [],
},
{
    "name": "stock_hk_hot_rank_detail_realtime_em",
    "display_name": "港股",
    "description": "港股数据",
    "route": "/stocks/collections/stock_hk_hot_rank_detail_realtime_em",
    "fields": [],
},
{
    "name": "stock_hk_hot_rank_em",
    "display_name": "人气榜-港股",
    "description": "人气榜-港股数据",
    "route": "/stocks/collections/stock_hk_hot_rank_em",
    "fields": [],
},
{
    "name": "stock_hk_hot_rank_latest_em",
    "display_name": "港股",
    "description": "港股数据",
    "route": "/stocks/collections/stock_hk_hot_rank_latest_em",
    "fields": [],
},
{
    "name": "stock_hk_indicator_eniu",
    "display_name": "港股个股指标",
    "description": "港股个股指标数据",
    "route": "/stocks/collections/stock_hk_indicator_eniu",
    "fields": [],
},
{
    "name": "stock_hk_main_board_spot_em",
    "display_name": "港股主板实时行情数据-东财",
    "description": "港股主板实时行情数据-东财数据",
    "route": "/stocks/collections/stock_hk_main_board_spot_em",
    "fields": [],
},
{
    "name": "stock_hk_profit_forecast_et",
    "display_name": "港股盈利预测-经济通",
    "description": "港股盈利预测-经济通数据",
    "route": "/stocks/collections/stock_hk_profit_forecast_et",
    "fields": [],
},
{
    "name": "stock_hk_scale_comparison_em",
    "display_name": "规模对比",
    "description": "规模对比数据",
    "route": "/stocks/collections/stock_hk_scale_comparison_em",
    "fields": [],
},
{
    "name": "stock_hk_security_profile_em",
    "display_name": "证券资料",
    "description": "证券资料数据",
    "route": "/stocks/collections/stock_hk_security_profile_em",
    "fields": [],
},
{
    "name": "stock_hk_spot",
    "display_name": "港股实时行情-新浪",
    "description": "新浪的港股实时行情数据",
    "route": "/stocks/collections/stock_hk_spot",
    "fields": [],
    "source": "新浪财经",
    "category": "港股数据",
    "update_frequency": "实时"
},
{
    "name": "stock_hk_spot_em",
    "display_name": "港股实时行情-东方财富",
    "description": "东方财富的港股实时行情数据",
    "route": "/stocks/collections/stock_hk_spot_em",
    "fields": [],
    "source": "东方财富",
    "category": "港股数据",
    "update_frequency": "实时"
},
{
    "name": "stock_hk_valuation_baidu",
    "display_name": "港股估值指标",
    "description": "百度财经的港股估值指标数据",
    "route": "/stocks/collections/stock_hk_valuation_baidu",
    "fields": [],
    "source": "百度财经",
    "category": "港股数据",
    "update_frequency": "每日"
},
{
    "name": "stock_hk_valuation_comparison_em",
    "display_name": "港股估值对比",
    "description": "东方财富的港股估值对比数据",
    "route": "/stocks/collections/stock_hk_valuation_comparison_em",
    "fields": [],
    "source": "东方财富",
    "category": "港股数据",
    "update_frequency": "每日"
},
{
    "name": "stock_hold_change_cninfo",
    "display_name": "股本变动",
    "description": "股本变动数据",
    "route": "/stocks/collections/stock_hold_change_cninfo",
    "fields": [],
},
{
    "name": "stock_hold_control_cninfo",
    "display_name": "实际控制人持股变动",
    "description": "实际控制人持股变动数据",
    "route": "/stocks/collections/stock_hold_control_cninfo",
    "fields": [],
},
{
    "name": "stock_hold_management_detail_cninfo",
    "display_name": "高管持股变动明细",
    "description": "高管持股变动明细数据",
    "route": "/stocks/collections/stock_hold_management_detail_cninfo",
    "fields": [],
},
{
    "name": "stock_hold_management_detail_em",
    "display_name": "董监高及相关人员持股变动明细",
    "description": "董监高及相关人员持股变动明细数据",
    "route": "/stocks/collections/stock_hold_management_detail_em",
    "fields": [],
},
{
    "name": "stock_hold_management_person_em",
    "display_name": "人员增减持股变动明细",
    "description": "人员增减持股变动明细数据",
    "route": "/stocks/collections/stock_hold_management_person_em",
    "fields": [],
},
{
    "name": "stock_hold_num_cninfo",
    "display_name": "股东人数及持股集中度",
    "description": "股东人数及持股集中度数据",
    "route": "/stocks/collections/stock_hold_num_cninfo",
    "fields": [],
},
{
    "name": "stock_hot_deal_xq",
    "display_name": "交易排行榜",
    "description": "交易排行榜数据",
    "route": "/stocks/collections/stock_hot_deal_xq",
    "fields": [],
},
{
    "name": "stock_hot_follow_xq",
    "display_name": "关注排行榜",
    "description": "关注排行榜数据",
    "route": "/stocks/collections/stock_hot_follow_xq",
    "fields": [],
},
{
    "name": "stock_hot_keyword_em",
    "display_name": "热门关键词",
    "description": "热门关键词数据",
    "route": "/stocks/collections/stock_hot_keyword_em",
    "fields": [],
},
{
    "name": "stock_hot_rank_detail_em",
    "display_name": "A股",
    "description": "A股数据",
    "route": "/stocks/collections/stock_hot_rank_detail_em",
    "fields": [],
},
{
    "name": "stock_hot_rank_detail_realtime_em",
    "display_name": "A股",
    "description": "A股数据",
    "route": "/stocks/collections/stock_hot_rank_detail_realtime_em",
    "fields": [],
},
{
    "name": "stock_hot_rank_em",
    "display_name": "人气榜-A股",
    "description": "人气榜-A股数据",
    "route": "/stocks/collections/stock_hot_rank_em",
    "fields": [],
},
{
    "name": "stock_hot_rank_latest_em",
    "display_name": "A股",
    "description": "A股数据",
    "route": "/stocks/collections/stock_hot_rank_latest_em",
    "fields": [],
},
{
    "name": "stock_hot_rank_relate_em",
    "display_name": "相关股票",
    "description": "相关股票数据",
    "route": "/stocks/collections/stock_hot_rank_relate_em",
    "fields": [],
},
{
    "name": "stock_hot_search_baidu",
    "display_name": "热搜股票",
    "description": "热搜股票数据",
    "route": "/stocks/collections/stock_hot_search_baidu",
    "fields": [],
},
{
    "name": "stock_hot_tweet_xq",
    "display_name": "讨论排行榜",
    "description": "讨论排行榜数据",
    "route": "/stocks/collections/stock_hot_tweet_xq",
    "fields": [],
},
{
    "name": "stock_hot_up_em",
    "display_name": "飙升榜-A股",
    "description": "飙升榜-A股数据",
    "route": "/stocks/collections/stock_hot_up_em",
    "fields": [],
},
{
    "name": "stock_hsgt_fund_flow_summary_em",
    "display_name": "沪深港通资金流向",
    "description": "沪深港通资金流向数据",
    "route": "/stocks/collections/stock_hsgt_fund_flow_summary_em",
    "fields": [],
},
{
    "name": "stock_index_pb_lg",
    "display_name": "指数市净率",
    "description": "指数市净率数据",
    "route": "/stocks/collections/stock_index_pb_lg",
    "fields": [],
},
{
    "name": "stock_index_pe_lg",
    "display_name": "指数市盈率",
    "description": "指数市盈率数据",
    "route": "/stocks/collections/stock_index_pe_lg",
    "fields": [],
},
{
    "name": "stock_individual_basic_info_hk_xq",
    "display_name": "个股信息查询-雪球",
    "description": "个股信息查询-雪球数据",
    "route": "/stocks/collections/stock_individual_basic_info_hk_xq",
    "fields": [],
},
{
    "name": "stock_individual_basic_info_us_xq",
    "display_name": "个股信息查询-雪球",
    "description": "个股信息查询-雪球数据",
    "route": "/stocks/collections/stock_individual_basic_info_us_xq",
    "fields": [],
},
{
    "name": "stock_individual_basic_info_xq",
    "display_name": "个股信息查询-雪球",
    "description": "个股信息查询-雪球数据",
    "route": "/stocks/collections/stock_individual_basic_info_xq",
    "fields": [],
},
{
    "name": "stock_individual_info_em",
    "display_name": "个股信息查询-东财",
    "description": "个股信息查询-东财数据",
    "route": "/stocks/collections/stock_individual_info_em",
    "fields": [],
},
{
    "name": "stock_individual_spot_xq",
    "display_name": "实时行情数据-雪球",
    "description": "实时行情数据-雪球数据",
    "route": "/stocks/collections/stock_individual_spot_xq",
    "fields": [],
},
{
    "name": "stock_industry_category_cninfo",
    "display_name": "行业分类数据-巨潮资讯",
    "description": "行业分类数据-巨潮资讯数据",
    "route": "/stocks/collections/stock_industry_category_cninfo",
    "fields": [],
},
{
    "name": "stock_industry_change_cninfo",
    "display_name": "上市公司行业归属的变动情况-巨潮资讯",
    "description": "上市公司行业归属的变动情况-巨潮资讯数据",
    "route": "/stocks/collections/stock_industry_change_cninfo",
    "fields": [],
},
{
    "name": "stock_industry_clf_hist_sw",
    "display_name": "申万个股行业分类变动历史",
    "description": "申万个股行业分类变动历史数据",
    "route": "/stocks/collections/stock_industry_clf_hist_sw",
    "fields": [],
},
{
    "name": "stock_industry_pe_ratio_cninfo",
    "display_name": "行业市盈率",
    "description": "行业市盈率数据",
    "route": "/stocks/collections/stock_industry_pe_ratio_cninfo",
    "fields": [],
},
{
    "name": "stock_info_a_code_name",
    "display_name": "股票列表-A股",
    "description": "股票列表-A股数据",
    "route": "/stocks/collections/stock_info_a_code_name",
    "fields": [],
},
{
    "name": "stock_info_bj_name_code",
    "display_name": "股票列表-北证",
    "description": "股票列表-北证数据",
    "route": "/stocks/collections/stock_info_bj_name_code",
    "fields": [],
},
{
    "name": "stock_info_change_name",
    "display_name": "股票更名",
    "description": "股票更名数据",
    "route": "/stocks/collections/stock_info_change_name",
    "fields": [],
},
{
    "name": "stock_info_sh_delist",
    "display_name": "暂停-终止上市-上证",
    "description": "暂停-终止上市-上证数据",
    "route": "/stocks/collections/stock_info_sh_delist",
    "fields": [],
},
{
    "name": "stock_info_sh_name_code",
    "display_name": "股票列表-上证",
    "description": "股票列表-上证数据",
    "route": "/stocks/collections/stock_info_sh_name_code",
    "fields": [],
},
{
    "name": "stock_info_sz_change_name",
    "display_name": "名称变更-深证",
    "description": "名称变更-深证数据",
    "route": "/stocks/collections/stock_info_sz_change_name",
    "fields": [],
},
{
    "name": "stock_info_sz_delist",
    "display_name": "终止-暂停上市-深证",
    "description": "终止-暂停上市-深证数据",
    "route": "/stocks/collections/stock_info_sz_delist",
    "fields": [],
},
{
    "name": "stock_info_sz_name_code",
    "display_name": "股票列表-深证",
    "description": "股票列表-深证数据",
    "route": "/stocks/collections/stock_info_sz_name_code",
    "fields": [],
},
{
    "name": "stock_inner_trade_xq",
    "display_name": "内部交易",
    "description": "内部交易数据",
    "route": "/stocks/collections/stock_inner_trade_xq",
    "fields": [],
},
{
    "name": "stock_institute_hold",
    "display_name": "机构持股一览表",
    "description": "机构持股一览表数据",
    "route": "/stocks/collections/stock_institute_hold",
    "fields": [],
},
{
    "name": "stock_institute_hold_detail",
    "display_name": "机构持股详情",
    "description": "机构持股详情数据",
    "route": "/stocks/collections/stock_institute_hold_detail",
    "fields": [],
},
{
    "name": "stock_institute_recommend",
    "display_name": "机构推荐池",
    "description": "机构推荐池数据",
    "route": "/stocks/collections/stock_institute_recommend",
    "fields": [],
},
{
    "name": "stock_institute_recommend_detail",
    "display_name": "股票评级记录",
    "description": "股票评级记录数据",
    "route": "/stocks/collections/stock_institute_recommend_detail",
    "fields": [],
},
{
    "name": "stock_intraday_em",
    "display_name": "日内分时数据-东财",
    "description": "日内分时数据-东财数据",
    "route": "/stocks/collections/stock_intraday_em",
    "fields": [],
},
{
    "name": "stock_intraday_sina",
    "display_name": "日内分时数据-新浪",
    "description": "日内分时数据-新浪数据",
    "route": "/stocks/collections/stock_intraday_sina",
    "fields": [],
},
{
    "name": "stock_ipo_benefit_ths",
    "display_name": "IPO 受益股",
    "description": "IPO 受益股数据",
    "route": "/stocks/collections/stock_ipo_benefit_ths",
    "fields": [],
},
{
    "name": "stock_ipo_declare",
    "display_name": "首发申报信息",
    "description": "首发申报信息数据",
    "route": "/stocks/collections/stock_ipo_declare",
    "fields": [],
},
{
    "name": "stock_ipo_summary_cninfo",
    "display_name": "上市相关-巨潮资讯",
    "description": "上市相关-巨潮资讯数据",
    "route": "/stocks/collections/stock_ipo_summary_cninfo",
    "fields": [],
},
{
    "name": "stock_irm_ans_cninfo",
    "display_name": "互动易-回答",
    "description": "互动易-回答数据",
    "route": "/stocks/collections/stock_irm_ans_cninfo",
    "fields": [],
},
{
    "name": "stock_irm_cninfo",
    "display_name": "互动易-提问",
    "description": "互动易-提问数据",
    "route": "/stocks/collections/stock_irm_cninfo",
    "fields": [],
},
{
    "name": "stock_kc_a_spot_em",
    "display_name": "科创板",
    "description": "科创板数据",
    "route": "/stocks/collections/stock_kc_a_spot_em",
    "fields": [],
},
{
    "name": "stock_lh_yyb_capital",
    "display_name": "龙虎榜-营业部排行-资金实力最强",
    "description": "龙虎榜-营业部排行-资金实力最强数据",
    "route": "/stocks/collections/stock_lh_yyb_capital",
    "fields": [],
},
{
    "name": "stock_lh_yyb_control",
    "display_name": "龙虎榜-营业部排行-抱团操作实力",
    "description": "龙虎榜-营业部排行-抱团操作实力数据",
    "route": "/stocks/collections/stock_lh_yyb_control",
    "fields": [],
},
{
    "name": "stock_lh_yyb_most",
    "display_name": "龙虎榜-营业部排行-上榜次数最多",
    "description": "龙虎榜-营业部排行-上榜次数最多数据",
    "route": "/stocks/collections/stock_lh_yyb_most",
    "fields": [],
},
{
    "name": "stock_lhb_detail_daily_sina",
    "display_name": "龙虎榜-每日详情",
    "description": "龙虎榜-每日详情数据",
    "route": "/stocks/collections/stock_lhb_detail_daily_sina",
    "fields": [],
},
{
    "name": "stock_lhb_detail_em",
    "display_name": "龙虎榜详情",
    "description": "龙虎榜详情数据",
    "route": "/stocks/collections/stock_lhb_detail_em",
    "fields": [],
},
{
    "name": "stock_lhb_ggtj_sina",
    "display_name": "龙虎榜-个股上榜统计",
    "description": "龙虎榜-个股上榜统计数据",
    "route": "/stocks/collections/stock_lhb_ggtj_sina",
    "fields": [],
},
{
    "name": "stock_lhb_hyyyb_em",
    "display_name": "每日活跃营业部",
    "description": "每日活跃营业部数据",
    "route": "/stocks/collections/stock_lhb_hyyyb_em",
    "fields": [],
},
{
    "name": "stock_lhb_jgmmtj_em",
    "display_name": "机构买卖每日统计",
    "description": "机构买卖每日统计数据",
    "route": "/stocks/collections/stock_lhb_jgmmtj_em",
    "fields": [],
},
{
    "name": "stock_lhb_jgmx_sina",
    "display_name": "龙虎榜-机构席位成交明细",
    "description": "龙虎榜-机构席位成交明细数据",
    "route": "/stocks/collections/stock_lhb_jgmx_sina",
    "fields": [],
},
{
    "name": "stock_lhb_jgstatistic_em",
    "display_name": "机构席位追踪",
    "description": "机构席位追踪数据",
    "route": "/stocks/collections/stock_lhb_jgstatistic_em",
    "fields": [],
},
{
    "name": "stock_lhb_jgzz_sina",
    "display_name": "龙虎榜-机构席位追踪",
    "description": "龙虎榜-机构席位追踪数据",
    "route": "/stocks/collections/stock_lhb_jgzz_sina",
    "fields": [],
},
{
    "name": "stock_lhb_stock_detail_em",
    "display_name": "个股龙虎榜详情",
    "description": "个股龙虎榜详情数据",
    "route": "/stocks/collections/stock_lhb_stock_detail_em",
    "fields": [],
},
{
    "name": "stock_lhb_stock_statistic_em",
    "display_name": "个股上榜统计",
    "description": "个股上榜统计数据",
    "route": "/stocks/collections/stock_lhb_stock_statistic_em",
    "fields": [],
},
{
    "name": "stock_lhb_traderstatistic_em",
    "display_name": "营业部统计",
    "description": "营业部统计数据",
    "route": "/stocks/collections/stock_lhb_traderstatistic_em",
    "fields": [],
},
{
    "name": "stock_lhb_yyb_detail_em",
    "display_name": "营业部详情数据-东财",
    "description": "营业部详情数据-东财数据",
    "route": "/stocks/collections/stock_lhb_yyb_detail_em",
    "fields": [],
},
{
    "name": "stock_lhb_yybph_em",
    "display_name": "营业部排行",
    "description": "营业部排行数据",
    "route": "/stocks/collections/stock_lhb_yybph_em",
    "fields": [],
},
{
    "name": "stock_lhb_yytj_sina",
    "display_name": "龙虎榜营业上榜统计-新浪",
    "description": "新浪的龙虎榜营业上榜统计数据",
    "route": "/stocks/collections/stock_lhb_yytj_sina",
    "fields": [],
    "source": "新浪财经",
    "category": "龙虎榜数据",
    "update_frequency": "每日"
},
{
    "name": "stock_lrb_em",
    "display_name": "利润表-东方财富",
    "description": "东方财富的利润表数据",
    "route": "/stocks/collections/stock_lrb_em",
    "fields": [],
    "source": "东方财富",
    "category": "财务数据",
    "update_frequency": "季度"
},
{
    "name": "stock_main_stock_holder",
    "display_name": "主要股东",
    "description": "主要股东数据",
    "route": "/stocks/collections/stock_main_stock_holder",
    "fields": [],
    "source": "akshare",
    "category": "股东数据",
    "update_frequency": "季度"
},
{
    "name": "stock_margin_account_info",
    "display_name": "两融账户信息",
    "description": "两融账户信息数据",
    "route": "/stocks/collections/stock_margin_account_info",
    "fields": [],
},
{
    "name": "stock_margin_detail_sse",
    "display_name": "融资融券明细",
    "description": "融资融券明细数据",
    "route": "/stocks/collections/stock_margin_detail_sse",
    "fields": [],
},
{
    "name": "stock_margin_detail_szse",
    "display_name": "融资融券明细",
    "description": "融资融券明细数据",
    "route": "/stocks/collections/stock_margin_detail_szse",
    "fields": [],
},
{
    "name": "stock_margin_ratio_pa",
    "display_name": "标的证券名单及保证金比例查询",
    "description": "标的证券名单及保证金比例查询数据",
    "route": "/stocks/collections/stock_margin_ratio_pa",
    "fields": [],
},
{
    "name": "stock_margin_sse",
    "display_name": "融资融券汇总",
    "description": "融资融券汇总数据",
    "route": "/stocks/collections/stock_margin_sse",
    "fields": [],
},
{
    "name": "stock_margin_szse",
    "display_name": "融资融券汇总",
    "description": "融资融券汇总数据",
    "route": "/stocks/collections/stock_margin_szse",
    "fields": [],
},
{
    "name": "stock_margin_underlying_info_szse",
    "display_name": "标的证券信息",
    "description": "标的证券信息数据",
    "route": "/stocks/collections/stock_margin_underlying_info_szse",
    "fields": [],
},
{
    "name": "stock_market_activity_legu",
    "display_name": "赚钱效应分析",
    "description": "赚钱效应分析数据",
    "route": "/stocks/collections/stock_market_activity_legu",
    "fields": [],
},
{
    "name": "stock_market_pb_lg",
    "display_name": "主板市净率",
    "description": "主板市净率数据",
    "route": "/stocks/collections/stock_market_pb_lg",
    "fields": [],
},
{
    "name": "stock_market_pe_lg",
    "display_name": "主板市盈率",
    "description": "主板市盈率数据",
    "route": "/stocks/collections/stock_market_pe_lg",
    "fields": [],
},
{
    "name": "stock_new_a_spot_em",
    "display_name": "新股",
    "description": "新股数据",
    "route": "/stocks/collections/stock_new_a_spot_em",
    "fields": [],
},
{
    "name": "stock_new_gh_cninfo",
    "display_name": "新股过会",
    "description": "新股过会数据",
    "route": "/stocks/collections/stock_new_gh_cninfo",
    "fields": [],
},
{
    "name": "stock_new_ipo_cninfo",
    "display_name": "新股发行",
    "description": "新股发行数据",
    "route": "/stocks/collections/stock_new_ipo_cninfo",
    "fields": [],
},
{
    "name": "stock_news_main_cx",
    "display_name": "财经内容精选",
    "description": "财经内容精选数据",
    "route": "/stocks/collections/stock_news_main_cx",
    "fields": [],
},
{
    "name": "stock_pg_em",
    "display_name": "配股",
    "description": "配股数据",
    "route": "/stocks/collections/stock_pg_em",
    "fields": [],
},
{
    "name": "stock_price_js",
    "display_name": "美港目标价",
    "description": "美港目标价数据",
    "route": "/stocks/collections/stock_price_js",
    "fields": [],
},
{
    "name": "stock_profile_cninfo",
    "display_name": "公司概况-巨潮资讯",
    "description": "公司概况-巨潮资讯数据",
    "route": "/stocks/collections/stock_profile_cninfo",
    "fields": [],
},
{
    "name": "stock_profit_forecast_em",
    "display_name": "盈利预测-东方财富",
    "description": "盈利预测-东方财富数据",
    "route": "/stocks/collections/stock_profit_forecast_em",
    "fields": [],
},
{
    "name": "stock_profit_forecast_ths",
    "display_name": "盈利预测-同花顺",
    "description": "盈利预测-同花顺数据",
    "route": "/stocks/collections/stock_profit_forecast_ths",
    "fields": [],
},
{
    "name": "stock_profit_sheet_by_report_em",
    "display_name": "利润表-按报告期",
    "description": "利润表-按报告期数据",
    "route": "/stocks/collections/stock_profit_sheet_by_report_em",
    "fields": [],
},
{
    "name": "stock_profit_sheet_by_yearly_em",
    "display_name": "利润表-按年度",
    "description": "利润表-按年度数据",
    "route": "/stocks/collections/stock_profit_sheet_by_yearly_em",
    "fields": [],
},
{
    "name": "stock_qbzf_em",
    "display_name": "增发",
    "description": "增发数据",
    "route": "/stocks/collections/stock_qbzf_em",
    "fields": [],
},
{
    "name": "stock_qsjy_em",
    "display_name": "券商业绩月报",
    "description": "券商业绩月报数据",
    "route": "/stocks/collections/stock_qsjy_em",
    "fields": [],
},
{
    "name": "stock_rank_cxfl_ths",
    "display_name": "持续放量",
    "description": "持续放量数据",
    "route": "/stocks/collections/stock_rank_cxfl_ths",
    "fields": [],
},
{
    "name": "stock_rank_cxsl_ths",
    "display_name": "持续缩量",
    "description": "持续缩量数据",
    "route": "/stocks/collections/stock_rank_cxsl_ths",
    "fields": [],
},
{
    "name": "stock_rank_forecast_cninfo",
    "display_name": "投资评级",
    "description": "投资评级数据",
    "route": "/stocks/collections/stock_rank_forecast_cninfo",
    "fields": [],
},
{
    "name": "stock_rank_ljqd_ths",
    "display_name": "量价齐跌",
    "description": "量价齐跌数据",
    "route": "/stocks/collections/stock_rank_ljqd_ths",
    "fields": [],
},
{
    "name": "stock_rank_ljqs_ths",
    "display_name": "量价齐升",
    "description": "量价齐升数据",
    "route": "/stocks/collections/stock_rank_ljqs_ths",
    "fields": [],
},
{
    "name": "stock_rank_xstp_ths",
    "display_name": "向上突破",
    "description": "向上突破数据",
    "route": "/stocks/collections/stock_rank_xstp_ths",
    "fields": [],
},
{
    "name": "stock_rank_xxtp_ths",
    "display_name": "向下突破",
    "description": "向下突破数据",
    "route": "/stocks/collections/stock_rank_xxtp_ths",
    "fields": [],
},
{
    "name": "stock_rank_xzjp_ths",
    "display_name": "险资举牌",
    "description": "险资举牌数据",
    "route": "/stocks/collections/stock_rank_xzjp_ths",
    "fields": [],
},
{
    "name": "stock_register_bj",
    "display_name": "北交所",
    "description": "北交所数据",
    "route": "/stocks/collections/stock_register_bj",
    "fields": [],
},
{
    "name": "stock_register_cyb",
    "display_name": "创业板",
    "description": "创业板数据",
    "route": "/stocks/collections/stock_register_cyb",
    "fields": [],
},
{
    "name": "stock_register_db",
    "display_name": "达标企业",
    "description": "达标企业数据",
    "route": "/stocks/collections/stock_register_db",
    "fields": [],
},
{
    "name": "stock_register_kcb",
    "display_name": "科创板",
    "description": "科创板数据",
    "route": "/stocks/collections/stock_register_kcb",
    "fields": [],
},
{
    "name": "stock_register_sh",
    "display_name": "上海主板",
    "description": "上海主板数据",
    "route": "/stocks/collections/stock_register_sh",
    "fields": [],
},
{
    "name": "stock_register_sz",
    "display_name": "深圳主板",
    "description": "深圳主板数据",
    "route": "/stocks/collections/stock_register_sz",
    "fields": [],
},
{
    "name": "stock_report_disclosure",
    "display_name": "预约披露时间-巨潮资讯",
    "description": "预约披露时间-巨潮资讯数据",
    "route": "/stocks/collections/stock_report_disclosure",
    "fields": [],
},
{
    "name": "stock_report_fund_hold",
    "display_name": "基金持股",
    "description": "基金持股数据",
    "route": "/stocks/collections/stock_report_fund_hold",
    "fields": [],
},
{
    "name": "stock_report_fund_hold_detail",
    "display_name": "基金持股明细",
    "description": "基金持股明细数据",
    "route": "/stocks/collections/stock_report_fund_hold_detail",
    "fields": [],
},
{
    "name": "stock_repurchase_em",
    "display_name": "股票回购数据",
    "description": "股票回购数据数据",
    "route": "/stocks/collections/stock_repurchase_em",
    "fields": [],
},
{
    "name": "stock_restricted_release_detail_em",
    "display_name": "限售股解禁详情",
    "description": "限售股解禁详情数据",
    "route": "/stocks/collections/stock_restricted_release_detail_em",
    "fields": [],
},
{
    "name": "stock_restricted_release_queue_sina",
    "display_name": "个股限售解禁-新浪",
    "description": "个股限售解禁-新浪数据",
    "route": "/stocks/collections/stock_restricted_release_queue_sina",
    "fields": [],
},
{
    "name": "stock_restricted_release_stockholder_em",
    "display_name": "解禁股东",
    "description": "解禁股东数据",
    "route": "/stocks/collections/stock_restricted_release_stockholder_em",
    "fields": [],
},
{
    "name": "stock_restricted_release_summary_em",
    "display_name": "限售股解禁",
    "description": "限售股解禁数据",
    "route": "/stocks/collections/stock_restricted_release_summary_em",
    "fields": [],
},
{
    "name": "stock_sector_detail",
    "display_name": "板块详情",
    "description": "板块详情数据",
    "route": "/stocks/collections/stock_sector_detail",
    "fields": [],
},
{
    "name": "stock_sector_spot",
    "display_name": "板块行情",
    "description": "板块行情数据",
    "route": "/stocks/collections/stock_sector_spot",
    "fields": [],
},
{
    "name": "stock_sgt_settlement_exchange_rate_sse",
    "display_name": "结算汇率-沪港通",
    "description": "结算汇率-沪港通数据",
    "route": "/stocks/collections/stock_sgt_settlement_exchange_rate_sse",
    "fields": [],
},
{
    "name": "stock_sgt_settlement_exchange_rate_szse",
    "display_name": "结算汇率-深港通",
    "description": "结算汇率-深港通数据",
    "route": "/stocks/collections/stock_sgt_settlement_exchange_rate_szse",
    "fields": [],
},
{
    "name": "stock_sh_a_spot_em",
    "display_name": "沪 A 股",
    "description": "沪 A 股数据",
    "route": "/stocks/collections/stock_sh_a_spot_em",
    "fields": [],
},
{
    "name": "stock_share_change_cninfo",
    "display_name": "公司股本变动-巨潮资讯",
    "description": "公司股本变动-巨潮资讯数据",
    "route": "/stocks/collections/stock_share_change_cninfo",
    "fields": [],
},
{
    "name": "stock_share_hold_change_bse",
    "display_name": "董监高及相关人员持股变动-北证",
    "description": "董监高及相关人员持股变动-北证数据",
    "route": "/stocks/collections/stock_share_hold_change_bse",
    "fields": [],
},
{
    "name": "stock_share_hold_change_sse",
    "display_name": "董监高及相关人员持股变动-上证",
    "description": "董监高及相关人员持股变动-上证数据",
    "route": "/stocks/collections/stock_share_hold_change_sse",
    "fields": [],
},
{
    "name": "stock_share_hold_change_szse",
    "display_name": "董监高及相关人员持股变动-深证",
    "description": "董监高及相关人员持股变动-深证数据",
    "route": "/stocks/collections/stock_share_hold_change_szse",
    "fields": [],
},
{
    "name": "stock_sns_sseinfo",
    "display_name": "上证e互动",
    "description": "上证e互动数据",
    "route": "/stocks/collections/stock_sns_sseinfo",
    "fields": [],
},
{
    "name": "stock_sse_deal_daily",
    "display_name": "上海证券交易所-每日概况",
    "description": "上海证券交易所-每日概况数据",
    "route": "/stocks/collections/stock_sse_deal_daily",
    "fields": [],
},
{
    "name": "stock_sse_summary",
    "display_name": "上海证券交易所",
    "description": "上海证券交易所数据",
    "route": "/stocks/collections/stock_sse_summary",
    "fields": [],
},
{
    "name": "stock_staq_net_stop",
    "display_name": "两网及退市",
    "description": "两网及退市数据",
    "route": "/stocks/collections/stock_staq_net_stop",
    "fields": [],
},
{
    "name": "stock_sy_em",
    "display_name": "个股商誉明细",
    "description": "个股商誉明细数据",
    "route": "/stocks/collections/stock_sy_em",
    "fields": [],
},
{
    "name": "stock_sy_hy_em",
    "display_name": "行业商誉",
    "description": "行业商誉数据",
    "route": "/stocks/collections/stock_sy_hy_em",
    "fields": [],
},
{
    "name": "stock_sy_jz_em",
    "display_name": "个股商誉减值明细",
    "description": "个股商誉减值明细数据",
    "route": "/stocks/collections/stock_sy_jz_em",
    "fields": [],
},
{
    "name": "stock_sy_profile_em",
    "display_name": "A股商誉市场概况",
    "description": "A股商誉市场概况数据",
    "route": "/stocks/collections/stock_sy_profile_em",
    "fields": [],
},
{
    "name": "stock_sy_yq_em",
    "display_name": "商誉减值预期明细",
    "description": "商誉减值预期明细数据",
    "route": "/stocks/collections/stock_sy_yq_em",
    "fields": [],
},
{
    "name": "stock_sz_a_spot_em",
    "display_name": "深 A 股",
    "description": "深 A 股数据",
    "route": "/stocks/collections/stock_sz_a_spot_em",
    "fields": [],
},
{
    "name": "stock_szse_area_summary",
    "display_name": "地区交易排序",
    "description": "地区交易排序数据",
    "route": "/stocks/collections/stock_szse_area_summary",
    "fields": [],
},
{
    "name": "stock_szse_sector_summary",
    "display_name": "股票行业成交",
    "description": "股票行业成交数据",
    "route": "/stocks/collections/stock_szse_sector_summary",
    "fields": [],
},
{
    "name": "stock_szse_summary",
    "display_name": "证券类别统计",
    "description": "证券类别统计数据",
    "route": "/stocks/collections/stock_szse_summary",
    "fields": [],
},
{
    "name": "stock_us_daily",
    "display_name": "美股历史行情-新浪",
    "description": "新浪的美股历史行情数据",
    "route": "/stocks/collections/stock_us_daily",
    "fields": [],
    "source": "新浪财经",
    "category": "美股数据",
    "update_frequency": "每日"
},
{
    "name": "stock_us_famous_spot_em",
    "display_name": "知名美股实时行情-东方财富",
    "description": "东方财富的知名美股实时行情数据",
    "route": "/stocks/collections/stock_us_famous_spot_em",
    "fields": [],
    "source": "东方财富",
    "category": "美股数据",
    "update_frequency": "实时"
},
{
    "name": "stock_us_hist",
    "display_name": "美股历史行情-东方财富",
    "description": "东方财富的美股历史行情数据",
    "route": "/stocks/collections/stock_us_hist",
    "fields": [],
    "source": "东方财富",
    "category": "美股数据",
    "update_frequency": "每日"
},
{
    "name": "stock_us_hist_min_em",
    "display_name": "分时数据-东财",
    "description": "分时数据-东财数据",
    "route": "/stocks/collections/stock_us_hist_min_em",
    "fields": [],
},
{
    "name": "stock_us_pink_spot_em",
    "display_name": "粉单市场",
    "description": "粉单市场数据",
    "route": "/stocks/collections/stock_us_pink_spot_em",
    "fields": [],
},
{
    "name": "stock_us_spot",
    "display_name": "实时行情数据-新浪",
    "description": "实时行情数据-新浪数据",
    "route": "/stocks/collections/stock_us_spot",
    "fields": [],
},
{
    "name": "stock_us_spot_em",
    "display_name": "实时行情数据-东财",
    "description": "实时行情数据-东财数据",
    "route": "/stocks/collections/stock_us_spot_em",
    "fields": [],
},
{
    "name": "stock_value_em",
    "display_name": "个股估值",
    "description": "个股估值数据",
    "route": "/stocks/collections/stock_value_em",
    "fields": [],
},
{
    "name": "stock_xgsr_ths",
    "display_name": "新股上市首日",
    "description": "新股上市首日数据",
    "route": "/stocks/collections/stock_xgsr_ths",
    "fields": [],
},
{
    "name": "stock_xjll_em",
    "display_name": "现金流量表",
    "description": "现金流量表数据",
    "route": "/stocks/collections/stock_xjll_em",
    "fields": [],
},
{
    "name": "stock_yjbb_em",
    "display_name": "业绩报表",
    "description": "业绩报表数据",
    "route": "/stocks/collections/stock_yjbb_em",
    "fields": [],
},
{
    "name": "stock_yjkb_em",
    "display_name": "业绩快报",
    "description": "业绩快报数据",
    "route": "/stocks/collections/stock_yjkb_em",
    "fields": [],
},
{
    "name": "stock_yzxdr_em",
    "display_name": "一致行动人",
    "description": "一致行动人数据",
    "route": "/stocks/collections/stock_yzxdr_em",
    "fields": [],
},
{
    "name": "stock_zcfz_bj_em",
    "display_name": "资产负债表-北交所",
    "description": "资产负债表-北交所数据",
    "route": "/stocks/collections/stock_zcfz_bj_em",
    "fields": [],
},
{
    "name": "stock_zcfz_em",
    "display_name": "资产负债表-沪深",
    "description": "资产负债表-沪深数据",
    "route": "/stocks/collections/stock_zcfz_em",
    "fields": [],
},
{
    "name": "stock_zh_a_cdr_daily",
    "display_name": "历史行情数据",
    "description": "历史行情数据数据",
    "route": "/stocks/collections/stock_zh_a_cdr_daily",
    "fields": [],
},
{
    "name": "stock_zh_a_daily",
    "display_name": "历史行情数据-新浪",
    "description": "历史行情数据-新浪数据",
    "route": "/stocks/collections/stock_zh_a_daily",
    "fields": [],
},
{
    "name": "stock_zh_a_disclosure_relation_cninfo",
    "display_name": "信息披露调研-巨潮资讯",
    "description": "信息披露调研-巨潮资讯数据",
    "route": "/stocks/collections/stock_zh_a_disclosure_relation_cninfo",
    "fields": [],
},
{
    "name": "stock_zh_a_disclosure_report_cninfo",
    "display_name": "信息披露公告-巨潮资讯",
    "description": "信息披露公告-巨潮资讯数据",
    "route": "/stocks/collections/stock_zh_a_disclosure_report_cninfo",
    "fields": [],
},
{
    "name": "stock_zh_a_gbjg_em",
    "display_name": "股本结构",
    "description": "股本结构数据",
    "route": "/stocks/collections/stock_zh_a_gbjg_em",
    "fields": [],
},
{
    "name": "stock_zh_a_gdhs",
    "display_name": "股东户数",
    "description": "股东户数数据",
    "route": "/stocks/collections/stock_zh_a_gdhs",
    "fields": [],
},
{
    "name": "stock_zh_a_gdhs_detail_em",
    "display_name": "股东户数详情",
    "description": "股东户数详情数据",
    "route": "/stocks/collections/stock_zh_a_gdhs_detail_em",
    "fields": [],
},
{
    "name": "stock_zh_a_hist",
    "display_name": "A股历史行情-东财",
    "description": "A股历史行情-东财数据",
    "route": "/stocks/collections/stock_zh_a_hist",
    "fields": [],
},
{
    "name": "stock_zh_a_hist_min_em",
    "display_name": "A股分时数据-东财",
    "description": "A股分时数据-东财数据",
    "route": "/stocks/collections/stock_zh_a_hist_min_em",
    "fields": [],
},
{
    "name": "stock_zh_a_hist_pre_min_em",
    "display_name": "盘前数据",
    "description": "盘前数据数据",
    "route": "/stocks/collections/stock_zh_a_hist_pre_min_em",
    "fields": [],
},
{
    "name": "stock_zh_a_hist_tx",
    "display_name": "历史行情数据-腾讯",
    "description": "历史行情数据-腾讯数据",
    "route": "/stocks/collections/stock_zh_a_hist_tx",
    "fields": [],
},
{
    "name": "stock_zh_a_minute",
    "display_name": "分时数据-新浪",
    "description": "分时数据-新浪数据",
    "route": "/stocks/collections/stock_zh_a_minute",
    "fields": [],
},
{
    "name": "stock_zh_a_new_em",
    "display_name": "新股",
    "description": "新股数据",
    "route": "/stocks/collections/stock_zh_a_new_em",
    "fields": [],
},
{
    "name": "stock_zh_a_spot",
    "display_name": "实时行情数据-新浪",
    "description": "实时行情数据-新浪数据",
    "route": "/stocks/collections/stock_zh_a_spot",
    "fields": [],
},
{
    "name": "stock_zh_a_spot_em",
    "display_name": "沪深京A股实时行情-东财",
    "description": "沪深京A股实时行情-东财数据",
    "route": "/stocks/collections/stock_zh_a_spot_em",
    "fields": [],
},
{
    "name": "stock_zh_a_st_em",
    "display_name": "风险警示板",
    "description": "风险警示板数据",
    "route": "/stocks/collections/stock_zh_a_st_em",
    "fields": [],
},
{
    "name": "stock_zh_a_stop_em",
    "display_name": "两网及退市",
    "description": "两网及退市数据",
    "route": "/stocks/collections/stock_zh_a_stop_em",
    "fields": [],
},
{
    "name": "stock_zh_a_tick_tx",
    "display_name": "腾讯财经",
    "description": "腾讯财经数据",
    "route": "/stocks/collections/stock_zh_a_tick_tx",
    "fields": [],
},
{
    "name": "stock_zh_ab_comparison_em",
    "display_name": "AB 股比价",
    "description": "AB 股比价数据",
    "route": "/stocks/collections/stock_zh_ab_comparison_em",
    "fields": [],
},
{
    "name": "stock_zh_ah_daily",
    "display_name": "历史行情数据",
    "description": "历史行情数据数据",
    "route": "/stocks/collections/stock_zh_ah_daily",
    "fields": [],
},
{
    "name": "stock_zh_ah_name",
    "display_name": "A+H股票字典",
    "description": "A+H股票字典数据",
    "route": "/stocks/collections/stock_zh_ah_name",
    "fields": [],
},
{
    "name": "stock_zh_ah_spot",
    "display_name": "实时行情数据-腾讯",
    "description": "实时行情数据-腾讯数据",
    "route": "/stocks/collections/stock_zh_ah_spot",
    "fields": [],
},
{
    "name": "stock_zh_ah_spot_em",
    "display_name": "实时行情数据-东财",
    "description": "实时行情数据-东财数据",
    "route": "/stocks/collections/stock_zh_ah_spot_em",
    "fields": [],
},
{
    "name": "stock_zh_b_daily",
    "display_name": "历史行情数据",
    "description": "历史行情数据数据",
    "route": "/stocks/collections/stock_zh_b_daily",
    "fields": [],
},
{
    "name": "stock_zh_b_minute",
    "display_name": "分时数据",
    "description": "分时数据数据",
    "route": "/stocks/collections/stock_zh_b_minute",
    "fields": [],
},
{
    "name": "stock_zh_b_spot",
    "display_name": "实时行情数据-新浪",
    "description": "实时行情数据-新浪数据",
    "route": "/stocks/collections/stock_zh_b_spot",
    "fields": [],
},
{
    "name": "stock_zh_b_spot_em",
    "display_name": "实时行情数据-东财",
    "description": "实时行情数据-东财数据",
    "route": "/stocks/collections/stock_zh_b_spot_em",
    "fields": [],
},
{
    "name": "stock_zh_dupont_comparison_em",
    "display_name": "杜邦分析比较",
    "description": "杜邦分析比较数据",
    "route": "/stocks/collections/stock_zh_dupont_comparison_em",
    "fields": [],
},
{
    "name": "stock_zh_growth_comparison_em",
    "display_name": "成长性比较",
    "description": "成长性比较数据",
    "route": "/stocks/collections/stock_zh_growth_comparison_em",
    "fields": [],
},
{
    "name": "stock_zh_kcb_daily",
    "display_name": "历史行情数据",
    "description": "历史行情数据数据",
    "route": "/stocks/collections/stock_zh_kcb_daily",
    "fields": [],
},
{
    "name": "stock_zh_kcb_report_em",
    "display_name": "科创板公告",
    "description": "科创板公告数据",
    "route": "/stocks/collections/stock_zh_kcb_report_em",
    "fields": [],
},
{
    "name": "stock_zh_kcb_spot",
    "display_name": "实时行情数据",
    "description": "实时行情数据数据",
    "route": "/stocks/collections/stock_zh_kcb_spot",
    "fields": [],
},
{
    "name": "stock_zh_scale_comparison_em",
    "display_name": "公司规模",
    "description": "公司规模数据",
    "route": "/stocks/collections/stock_zh_scale_comparison_em",
    "fields": [],
},
{
    "name": "stock_zh_valuation_baidu",
    "display_name": "A 股估值指标",
    "description": "A 股估值指标数据",
    "route": "/stocks/collections/stock_zh_valuation_baidu",
    "fields": [],
},
{
    "name": "stock_zh_valuation_comparison_em",
    "display_name": "估值比较",
    "description": "估值比较数据",
    "route": "/stocks/collections/stock_zh_valuation_comparison_em",
    "fields": [],
},
{
    "name": "stock_zh_vote_baidu",
    "display_name": "涨跌投票",
    "description": "涨跌投票数据",
    "route": "/stocks/collections/stock_zh_vote_baidu",
    "fields": [],
},
{
    "name": "stock_zt_pool_dtgc_em",
    "display_name": "跌停股池-东方财富",
    "description": "东方财富的跌停股池数据",
    "route": "/stocks/collections/stock_zt_pool_dtgc_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zt_pool_em",
    "display_name": "涨停股池-东方财富",
    "description": "东方财富的涨停股池数据",
    "route": "/stocks/collections/stock_zt_pool_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zt_pool_previous_em",
    "display_name": "昨日涨停股池-东方财富",
    "description": "东方财富的昨日涨停股池数据",
    "route": "/stocks/collections/stock_zt_pool_previous_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zt_pool_strong_em",
    "display_name": "强势股池-东方财富",
    "description": "东方财富的强势股池数据",
    "route": "/stocks/collections/stock_zt_pool_strong_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zt_pool_sub_new_em",
    "display_name": "次新股池-东方财富",
    "description": "东方财富的次新股池数据",
    "route": "/stocks/collections/stock_zt_pool_sub_new_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zt_pool_zbgc_em",
    "display_name": "炸板股池-东方财富",
    "description": "东方财富的炸板股池数据",
    "route": "/stocks/collections/stock_zt_pool_zbgc_em",
    "fields": [],
    "source": "东方财富",
    "category": "涨停数据",
    "update_frequency": "实时"
},
{
    "name": "stock_zygc_em",
    "display_name": "主营构成-东方财富",
    "description": "东方财富的主营构成数据",
    "route": "/stocks/collections/stock_zygc_em",
    "fields": [],
    "source": "东方财富",
    "category": "财务数据",
    "update_frequency": "季度"
},
{
    "name": "stock_zyjs_ths",
    "display_name": "主营介绍-同花顺",
    "description": "同花顺的主营介绍数据",
    "route": "/stocks/collections/stock_zyjs_ths",
    "fields": [],
    "source": "同花顺",
    "category": "财务数据",
    "update_frequency": "季度"
},
]
    return collections


@router.get("/quotes/overview")
async def get_quotes_overview(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量，默认20，最大100"),
    sort_by: Optional[str] = Query("amount", description="排序字段，默认按成交额排序"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    keyword: Optional[str] = Query(None, description="按代码或名称模糊搜索"),
    current_user: dict = Depends(get_current_user),
):
    """获取股票行情概览列表（支持分页与搜索）

    - 数据来源：market_quotes + stock_basic_info
    - 支持分页：page/page_size
    - 支持按代码/名称关键字搜索
    """
    db = get_mongo_db()

    # 允许排序的字段白名单
    allowed_sort_fields = {"amount", "volume", "pct_chg", "close", "trade_date", "updated_at"}
    sort_key = sort_by if sort_by in allowed_sort_fields else "amount"
    sort_direction = -1 if sort_dir == "desc" else 1

    try:
        # 构建基础查询条件
        query: Dict[str, Any] = {}

        # 如果提供了关键字，则先在 stock_basic_info 中查找匹配的代码
        if keyword:
            kw = keyword.strip()
            if kw:
                codes: List[str] = []
                basic_cursor = db["stock_basic_info"].find(
                    {
                        "$or": [
                            {"code": {"$regex": kw, "$options": "i"}},
                            {"name": {"$regex": kw, "$options": "i"}},
                        ]
                    },
                    {"_id": 0, "code": 1},
                )
                async for doc in basic_cursor:
                    code = doc.get("code")
                    if code and code not in codes:
                        codes.append(code)

                if codes:
                    query["$or"] = [
                        {"code": {"$in": codes}},
                        {"symbol": {"$in": codes}},
                    ]
                else:
                    # 没有匹配代码，直接返回空结果
                    return ok({"items": [], "total": 0, "page": page, "page_size": page_size})

        # 计算总数
        total = await db["market_quotes"].count_documents(query)

        # 分页查询
        skip = (page - 1) * page_size
        cursor = (
            db["market_quotes"]
            .find(
                query,
                {
                    "_id": 0,
                    "code": 1,
                    "symbol": 1,
                    "close": 1,
                    "pct_chg": 1,
                    "volume": 1,
                    "amount": 1,
                    "trade_date": 1,
                    "updated_at": 1,
                },
            )
            .sort(sort_key, sort_direction)
            .skip(skip)
            .limit(page_size)
        )
        quotes = await cursor.to_list(length=page_size)

        # 收集代码，用于补充名称和市场信息
        codes_for_basic: List[str] = []
        for q in quotes:
            code = q.get("code") or q.get("symbol")
            if code and code not in codes_for_basic:
                codes_for_basic.append(code)

        basic_map: Dict[str, Dict[str, Any]] = {}
        if codes_for_basic:
            basic_cursor = db["stock_basic_info"].find(
                {"code": {"$in": codes_for_basic}},
                {"_id": 0, "code": 1, "name": 1, "market": 1},
            )
            async for doc in basic_cursor:
                code = doc.get("code")
                if code:
                    basic_map[code] = doc

        items: List[Dict[str, Any]] = []
        for q in quotes:
            code = (q.get("code") or q.get("symbol") or "").strip()
            basic = basic_map.get(code, {})
            item = {
                "code": code,
                "name": basic.get("name"),
                "market": basic.get("market", "CN"),
                "latest_price": q.get("close"),
                "pct_chg": q.get("pct_chg"),
                "volume": q.get("volume"),
                "amount": q.get("amount"),
                "trade_date": q.get("trade_date"),
                "updated_at": q.get("updated_at"),
            }
            items.append(item)

        return ok({
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        })

    except Exception as e:
        logger.error(f"获取股票行情概览失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/collections/{collection_name}/data")
async def get_stock_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(20, ge=1, le=200, description="每页数量，默认20，最大200"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    code: Optional[str] = Query(None, description="按股票代码过滤"),
    current_user: dict = Depends(get_current_user),
):
    """获取指定股票数据集合的数据（分页）

    支持的集合名称：
    - stock_basic_info
    - market_quotes
    - stock_financial_data
    - stock_daily
    - stock_weekly
    - stock_monthly
    """
    db = get_mongo_db()

    collection_map = {
        "stock_basic_info": db["stock_basic_info"],
        "market_quotes": db["market_quotes"],
        "stock_financial_data": db["stock_financial_data"],
        "stock_daily": db["stock_daily"],
        "stock_weekly": db["stock_weekly"],
        "stock_monthly": db["stock_monthly"],
        "stock_sgt_reference_exchange_rate_szse": db["stock_sgt_reference_exchange_rate_szse"],
        "stock_sgt_reference_exchange_rate_sse": db["stock_sgt_reference_exchange_rate_sse"],
        "stock_hk_ggt_components_em": db["stock_hk_ggt_components_em"],
        "stock_hsgt_fund_min_em": db["stock_hsgt_fund_min_em"],
        "stock_hsgt_board_rank_em": db["stock_hsgt_board_rank_em"],
        "stock_hsgt_hold_stock_em": db["stock_hsgt_hold_stock_em"],
        "stock_hsgt_stock_statistics_em": db["stock_hsgt_stock_statistics_em"],
        "stock_hsgt_institution_statistics_em": db["stock_hsgt_institution_statistics_em"],
        "stock_hsgt_sh_hk_spot_em": db["stock_hsgt_sh_hk_spot_em"],
        "stock_hsgt_hist_em": db["stock_hsgt_hist_em"],
        "stock_hsgt_individual_em": db["stock_hsgt_individual_em"],
        "stock_hsgt_individual_detail_em": db["stock_hsgt_individual_detail_em"],
        "stock_em_hsgt_north_net_flow_in": db["stock_em_hsgt_north_net_flow_in"],
        "stock_em_hsgt_south_net_flow_in": db["stock_em_hsgt_south_net_flow_in"],
        "stock_em_hsgt_hold_stock": db["stock_em_hsgt_hold_stock"],
        "stock_tfp_em": db["stock_tfp_em"],
        "stock_zh_a_new": db["stock_zh_a_new"],
        "stock_ipo_info": db["stock_ipo_info"],
        "stock_xgsglb_em": db["stock_xgsglb_em"],
        "stock_dzjy_sctj": db["stock_dzjy_sctj"],
        "stock_dzjy_mrmx": db["stock_dzjy_mrmx"],
        "stock_dzjy_mrtj": db["stock_dzjy_mrtj"],
        "stock_jgdy_tj_em": db["stock_jgdy_tj_em"],
        "stock_jgdy_detail_em": db["stock_jgdy_detail_em"],
        "stock_jgcyd_em": db["stock_jgcyd_em"],
        "stock_gpzy_profile_em": db["stock_gpzy_profile_em"],
        "stock_news_em": db["stock_news_em"],
        "stock_js_weibo_nlp_time": db["stock_js_weibo_nlp_time"],
        "stock_cjrl_em": db["stock_cjrl_em"],
        "stock_yjfp_em": db["stock_yjfp_em"],
        "stock_yjyg_em": db["stock_yjyg_em"],
        "stock_yysj_em": db["stock_yysj_em"],
        "stock_add_stock_cninfo": db["stock_add_stock_cninfo"],
        "stock_restricted_release_queue_em": db["stock_restricted_release_queue_em"],
        "stock_info_change_name_em": db["stock_info_change_name_em"],
        "stock_board_industry_name_em": db["stock_board_industry_name_em"],
        "stock_gpgk_em": db["stock_gpgk_em"],
        "stock_fhps_detail_ths": db["stock_fhps_detail_ths"],
        "stock_hk_fhpx_detail_ths": db["stock_hk_fhpx_detail_ths"],
        "stock_fund_flow_individual": db["stock_fund_flow_individual"],
        "stock_fund_flow_concept": db["stock_fund_flow_concept"],
        "stock_fund_flow_industry": db["stock_fund_flow_industry"],
        "stock_fund_flow_big_deal": db["stock_fund_flow_big_deal"],
        "stock_individual_fund_flow": db["stock_individual_fund_flow"],
        "stock_individual_fund_flow_rank": db["stock_individual_fund_flow_rank"],
        "stock_market_fund_flow": db["stock_market_fund_flow"],
        "stock_sector_fund_flow_rank": db["stock_sector_fund_flow_rank"],
        "stock_main_fund_flow": db["stock_main_fund_flow"],
        "stock_sector_fund_flow_summary": db["stock_sector_fund_flow_summary"],
        "stock_sector_fund_flow_hist": db["stock_sector_fund_flow_hist"],
        "stock_concept_fund_flow_hist": db["stock_concept_fund_flow_hist"],
        "stock_cyq_em": db["stock_cyq_em"],
        "stock_gddh_em": db["stock_gddh_em"],
        "stock_zdhtmx_em": db["stock_zdhtmx_em"],
        "stock_research_report_em": db["stock_research_report_em"],
        "stock_notice_report": db["stock_notice_report"],
        "stock_financial_report_sina": db["stock_financial_report_sina"],
        "stock_balance_sheet_by_report_em": db["stock_balance_sheet_by_report_em"],
        "stock_profit_sheet_by_quarterly_em": db["stock_profit_sheet_by_quarterly_em"],
        "stock_cash_flow_sheet_by_report_em": db["stock_cash_flow_sheet_by_report_em"],
        "stock_cash_flow_sheet_by_yearly_em": db["stock_cash_flow_sheet_by_yearly_em"],
        "stock_cash_flow_sheet_by_quarterly_em": db["stock_cash_flow_sheet_by_quarterly_em"],
        "stock_financial_debt_ths": db["stock_financial_debt_ths"],
        "stock_financial_benefit_ths": db["stock_financial_benefit_ths"],
        "stock_financial_cash_ths": db["stock_financial_cash_ths"],
        "stock_balance_sheet_by_report_delisted_em": db["stock_balance_sheet_by_report_delisted_em"],
        "stock_profit_sheet_by_report_delisted_em": db["stock_profit_sheet_by_report_delisted_em"],
        "stock_cash_flow_sheet_by_report_delisted_em": db["stock_cash_flow_sheet_by_report_delisted_em"],
        "stock_financial_hk_report_em": db["stock_financial_hk_report_em"],
        "stock_financial_us_report_em": db["stock_financial_us_report_em"],
        "stock_financial_abstract": db["stock_financial_abstract"],
        "stock_financial_abstract_ths": db["stock_financial_abstract_ths"],
        "stock_financial_analysis_indicator_em": db["stock_financial_analysis_indicator_em"],
        "stock_financial_analysis_indicator": db["stock_financial_analysis_indicator"],
        "stock_financial_hk_analysis_indicator_em": db["stock_financial_hk_analysis_indicator_em"],
        "stock_financial_us_analysis_indicator_em": db["stock_financial_us_analysis_indicator_em"],
        "stock_history_dividend": db["stock_history_dividend"],
        "stock_gdfx_free_top_10_em": db["stock_gdfx_free_top_10_em"],
        "stock_gdfx_top_10_em": db["stock_gdfx_top_10_em"],
        "stock_gdfx_free_holding_change_em": db["stock_gdfx_free_holding_change_em"],
        "stock_gdfx_holding_change_em": db["stock_gdfx_holding_change_em"],
        "stock_management_change_ths": db["stock_management_change_ths"],
        "stock_shareholder_change_ths": db["stock_shareholder_change_ths"],
        "stock_gdfx_free_holding_analyse_em": db["stock_gdfx_free_holding_analyse_em"],
        "stock_gdfx_holding_analyse_em": db["stock_gdfx_holding_analyse_em"],
        # 添加新的股票数据集合
        "stock_individual_info_em": db["stock_individual_info_em"],
        "stock_individual_basic_info_xq": db["stock_individual_basic_info_xq"],
        "stock_zh_a_spot_em": db["stock_zh_a_spot_em"],
        "stock_zh_a_hist": db["stock_zh_a_hist"],
        "stock_zh_a_hist_min_em": db["stock_zh_a_hist_min_em"],
        "stock_bid_ask_em": db["stock_bid_ask_em"],
    }

    collection = collection_map.get(collection_name)
    if collection is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"集合 {collection_name} 不存在")

    try:
        # 构建查询条件
        query: Dict[str, Any] = {}
        if code:
            # 同时兼容 code 和 symbol 字段
            code6 = str(code).strip()
            query["$or"] = [{"code": code6}, {"symbol": code6}]

        # 获取总数
        total = await collection.count_documents(query)

        # 确定默认排序字段
        default_sort_key = None
        for date_field in ["trade_date", "date", "datetime", "timestamp", "report_period", "updated_at"]:
            test_doc = await collection.find_one({date_field: {"$exists": True}})
            if test_doc is not None:
                default_sort_key = date_field
                break

        if sort_by is not None:
            sort_key = sort_by
        elif default_sort_key is not None:
            sort_key = default_sort_key
        else:
            sort_key = "_id"
        sort_direction = -1 if sort_dir == "desc" else 1

        # 分页查询
        skip = (page - 1) * page_size
        cursor = collection.find(query).sort(sort_key, sort_direction).skip(skip).limit(page_size)

        items: List[Dict[str, Any]] = []
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)

        data = {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

        return ok(data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取股票集合 {collection_name} 数据失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/collections/{collection_name}/refresh")
async def refresh_stock_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    """刷新股票数据集合"""
    try:
        task_id = str(uuid.uuid4())
        task_manager = get_task_manager()
        task_manager.create_task(task_id, f"刷新{collection_name}")

        # 异步执行刷新任务
        refresh_service = StockRefreshService()
        background_tasks.add_task(
            refresh_service.refresh_collection,
            collection_name,
            task_id,
            params
        )

        return ok({
            "task_id": task_id,
            "message": f"刷新任务已启动"
        })
    except Exception as e:
        logger.error(f"启动刷新任务失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/collections/{collection_name}/refresh/status/{task_id}")
async def get_refresh_status(
    collection_name: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """查询刷新任务状态"""
    try:
        task_manager = get_task_manager()
        task_info = task_manager.get_task(task_id)

        if not task_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在")

        return ok(task_info)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询任务状态失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/collections/{collection_name}/stats")
async def get_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据统计信息"""
    try:
        db = get_mongo_db()
        collection = db[collection_name]

        total_count = await collection.count_documents({})

        # 获取最新和最旧的记录时间（如果有时间字段）
        stats = {
            "total_count": total_count,
            "collection_name": collection_name
        }

        # 尝试获取最新更新时间
        try:
            latest = await collection.find_one(
                {},
                sort=[("_id", -1)]
            )
            if latest and "_id" in latest:
                stats["latest_update"] = latest["_id"].generation_time.isoformat()
        except:
            pass

        return ok(stats)
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/collections/{collection_name}/clear")
async def clear_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空集合数据"""
    try:
        db = get_mongo_db()
        collection = db[collection_name]

        result = await collection.delete_many({})

        return ok({
            "deleted_count": result.deleted_count,
            "message": f"已清空 {collection_name}"
        })
    except Exception as e:
        logger.error(f"清空集合失败: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/collections/{collection_name}/upload")
async def upload_stock_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传股票数据文件"""
    try:
        if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
            return ok({"success": False, "error": "只支持CSV或Excel文件"})
            
        db = get_mongo_db()
        service = StockDataService()
        
        # Read file content
        content = await file.read()
        filename = file.filename
        
        result = await service.import_data_from_file(collection_name, content, filename)
        
        return ok(result)
    except Exception as e:
        logger.error(f"上传文件失败: {e}", exc_info=True)
        return ok({"success": False, "error": str(e)})


@router.post("/collections/{collection_name}/sync")
async def sync_stock_data(
    collection_name: str,
    sync_config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """远程同步股票数据"""
    try:
        db = get_mongo_db()
        service = StockDataService()
        
        result = await service.sync_data_from_remote(collection_name, sync_config)
        
        return ok(result)
    except Exception as e:
        logger.error(f"远程同步失败: {e}", exc_info=True)
        return ok({"success": False, "error": str(e)})


# ========== 自动生成的API路由 (290个集合 x 4个端点 = 1160个端点) ==========

@router.get("/collections/news_report_time_baidu")
async def get_news_report_time_baidu(
    skip: int = 0,
    limit: int = 100,
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_report_time_baidu/overview")
async def get_news_report_time_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取财报发行数据概览"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_report_time_baidu/refresh")
async def refresh_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """刷新财报发行数据"""
    from app.services.stock.news_report_time_baidu_service import NewsReportTimeBaiduService
    service = NewsReportTimeBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_report_time_baidu/clear")
async def clear_news_report_time_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
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
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_trade_notify_dividend_baidu/overview")
async def get_news_trade_notify_dividend_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取分红派息数据概览"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_trade_notify_dividend_baidu/refresh")
async def refresh_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """刷新分红派息数据"""
    from app.services.stock.news_trade_notify_dividend_baidu_service import NewsTradeNotifyDividendBaiduService
    service = NewsTradeNotifyDividendBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_trade_notify_dividend_baidu/clear")
async def clear_news_trade_notify_dividend_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
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
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取停复牌数据"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/news_trade_notify_suspend_baidu/overview")
async def get_news_trade_notify_suspend_baidu_overview(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取停复牌数据概览"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.get_overview()


@router.post("/collections/news_trade_notify_suspend_baidu/refresh")
async def refresh_news_trade_notify_suspend_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """刷新停复牌数据"""
    from app.services.stock.news_trade_notify_suspend_baidu_service import NewsTradeNotifySuspendBaiduService
    service = NewsTradeNotifySuspendBaiduService(db)
    return await service.refresh_data()


@router.delete("/collections/news_trade_notify_suspend_baidu/clear")
async def clear_news_trade_notify_suspend_baidu(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
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
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_data(skip=skip, limit=limit)


@router.get("/collections/stock_a_all_pb/overview")
async def get_stock_a_all_pb_overview(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """获取A 股等权重与中位数市净率数据概览"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.get_overview()


@router.post("/collections/stock_a_all_pb/refresh")
async def refresh_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """刷新A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.refresh_data()


@router.delete("/collections/stock_a_all_pb/clear")
async def clear_stock_a_all_pb(
    db: AsyncIOMotorClient = Depends(get_mongo_db)
):
    """清空A 股等权重与中位数市净率数据"""
    from app.services.stock.stock_a_all_pb_service import StockAAllPbService
    service = StockAAllPbService(db)
    return await service.clear_data()