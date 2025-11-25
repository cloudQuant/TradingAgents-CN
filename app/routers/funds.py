from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status, Body, UploadFile, File
from pydantic import BaseModel
import hashlib
import logging
import uuid
import asyncio
from fastapi.responses import JSONResponse

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.fund_refresh_service import FundRefreshService
from app.services.fund_data_service import FundDataService
from app.config.fund_update_config import get_collection_update_config

router = APIRouter(prefix="/api/funds", tags=["funds"])
logger = logging.getLogger("webapi")

# 简单的内存缓存
_fund_list_cache = {}
_cache_ttl_seconds = 300  # 5分钟缓存

# 集合字段顺序缓存
_collection_fields_cache = {}


def _get_collection_fields_order(collection_name: str) -> list:
    """获取集合的预定义字段顺序"""
    # 定义各集合的字段顺序（与 list_fund_collections 中定义一致）
    COLLECTION_FIELDS = {
        "fund_name_em": ["基金代码", "拼音缩写", "基金简称", "基金类型", "拼音全称"],
        "fund_basic_info": ["基金代码", "基金名称", "基金全称", "成立时间", "最新规模", "基金公司", "基金经理", "基金类型", "基金评级", "业绩比较基准"],
        "fund_info_index_em": ["基金代码", "基金名称", "单位净值", "日期", "日增长率", "近1周", "近1月", "近3月", "近6月", "近1年", "近2年", "近3年", "今年来", "成立来", "手续费", "起购金额", "跟踪标的", "跟踪方式"],
        "fund_purchase_status": ["序号", "基金代码", "基金简称", "基金类型", "最新净值/万份收益", "最新净值/万份收益-报告时间", "申购状态", "赎回状态", "下一开放日", "购买起点", "日累计限定金额", "手续费"],
        "fund_etf_spot_em": ["代码", "名称", "最新价", "IOPV实时估值", "基金折价率", "涨跌额", "涨跌幅", "成交量", "成交额", "开盘价", "最高价", "最低价", "昨收", "换手率", "量比", "委比", "外盘", "内盘", "主力净流入-净额", "主力净流入-净占比", "超大单净流入-净额", "超大单净流入-净占比", "大单净流入-净额", "大单净流入-净占比", "中单净流入-净额", "中单净流入-净占比", "小单净流入-净额", "小单净流入-净占比", "现手", "买一", "卖一", "最新份额", "流通市值", "总市值", "数据日期", "更新时间"],
        "fund_etf_spot_ths": ["序号", "基金代码", "基金名称", "当前-单位净值", "当前-累计净值", "前一日-单位净值", "前一日-累计净值", "增长值", "增长率", "赎回状态", "申购状态", "最新-交易日", "最新-单位净值", "最新-累计净值", "基金类型", "查询日期"],
        "fund_lof_spot_em": ["代码", "名称", "最新价", "涨跌额", "涨跌幅", "成交量", "成交额", "开盘价", "最高价", "最低价", "昨收", "换手率", "流通市值", "总市值", "数据日期"],
        "fund_portfolio_hold_em": ["基金代码", "股票代码", "股票名称", "季度", "持仓占比", "持仓数量", "持仓市值", "数据源", "接口名称", "更新时间"],
        "fund_portfolio_bond_hold_em": ["基金代码", "债券代码", "债券名称", "季度", "持仓占比", "持仓数量", "持仓市值", "code", "bond_code", "quarter", "source", "endpoint", "updated_at"],
        "fund_portfolio_industry_allocation_em": ["基金代码", "行业类别", "截止时间", "占净值比例", "code", "industry", "end_date", "source", "endpoint", "updated_at"],
        "fund_portfolio_change_em": ["序号", "股票代码", "股票名称", "本期累计买入金额", "占期初基金资产净值比例", "季度", "基金代码", "code", "stock_code", "quarter", "indicator_type", "source", "endpoint", "updated_at"],
        "fund_open_fund_rank_em": ["序号", "基金代码", "基金简称", "日期", "单位净值", "累计净值", "日增长率", "近1周", "近1月", "近3月", "近6月", "近1年", "近2年", "近3年", "今年来", "成立来", "自定义", "手续费", "code", "date", "source", "endpoint", "updated_at"],
        "fund_money_fund_daily_em": ["基金代码", "基金简称", "日期", "每万份收益", "7日年化收益率", "单位净值", "前一日万份收益", "前一日7日年化", "前一日净值", "日增长", "成立日期", "基金经理", "手续费", "申购状态"],
        "fund_etf_fund_daily_em": ["基金代码", "基金简称", "类型", "日期", "单位净值", "累计净值", "增长值", "增长率", "市价", "折价率"],
        "fund_value_estimation_em": ["序号", "基金代码", "基金名称", "估算数据-估算值", "估算数据-估算增长率", "公布数据-单位净值", "公布数据-日增长率", "估算偏差", "单位净值", "日期", "code", "date", "source", "endpoint", "updated_at"],
    }
    return COLLECTION_FIELDS.get(collection_name, [])


@router.get("/overview")
async def get_funds_overview(current_user: dict = Depends(get_current_user)):
    """获取基金概览数据"""
    try:
        db = get_mongo_db()
        
        # 统计数据
        stats = {
            "total_funds": 0,
            "categories": [],
            "recent_performance": {},
            "message": "基金概览功能正在开发中"
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取基金概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections")
async def list_fund_collections(current_user: dict = Depends(get_current_user)):
    """获取基金数据集合列表"""
    try:
        # 定义基金数据集合
        collections = [
            {
                "name": "fund_name_em",
                "display_name": "基金基本信息",
                "description": "东方财富网所有基金的基本信息，包括基金代码、简称、类型等",
                "route": "/funds/collections/fund_name_em",
                "fields": ["基金代码", "拼音缩写", "基金简称", "基金类型", "拼音全称"],
            },
            {
                "name": "fund_basic_info",
                "display_name": "雪球基金基本信息",
                "description": "雪球基金-基金详情，包括成立时间、最新规模、基金经理、评级等",
                "route": "/funds/collections/fund_basic_info",
                "fields": ["基金代码", "基金名称", "基金全称", "成立时间", "最新规模", "基金公司", "基金经理", "基金类型", "基金评级", "业绩比较基准"],
            },
            {
                "name": "fund_info_index_em",
                "display_name": "指数型基金基本信息",
                "description": "东方财富网-指数型基金基本信息，包括单位净值、日期、各周期业绩、手续费、起购金额、跟踪标的和方式等",
                "route": "/funds/collections/fund_info_index_em",
                "fields": [
                    "基金代码",
                    "基金名称",
                    "单位净值",
                    "日期",
                    "日增长率",
                    "近1周",
                    "近1月",
                    "近3月",
                    "近6月",
                    "近1年",
                    "近2年",
                    "近3年",
                    "今年来",
                    "成立来",
                    "手续费",
                    "起购金额",
                    "跟踪标的",
                    "跟踪方式",
                ],
            },
            {
                "name": "fund_net_value",
                "display_name": "基金净值数据",
                "description": "基金的历史净值数据",
                "route": "/funds/collections/fund_net_value",
                "fields": ["code", "date", "net_value", "accumulated_value", "growth_rate"],
            },
            {
                "name": "fund_ranking",
                "display_name": "基金排名",
                "description": "基金的业绩排名数据",
                "route": "/funds/collections/fund_ranking",
                "fields": ["code", "name", "ranking", "return_1m", "return_3m", "return_1y"],
            },
            {
                "name": "fund_purchase_status",
                "display_name": "基金申购状态",
                "description": "东方财富网-天天基金网-基金数据-基金申购状态，包括申购赎回状态、手续费、购买起点等",
                "route": "/funds/collections/fund_purchase_status",
                "fields": ["序号", "基金代码", "基金简称", "基金类型", "最新净值/万份收益", "最新净值/万份收益-报告时间", "申购状态", "赎回状态", "下一开放日", "购买起点", "日累计限定金额", "手续费"],
            },
            {
                "name": "fund_etf_spot_em",
                "display_name": "ETF基金实时行情-东财",
                "description": "东方财富网-ETF实时行情数据，包括最新价、涨跌幅、成交量、资金流向等",
                "route": "/funds/collections/fund_etf_spot_em",
                "fields": [
                    "代码", "名称", "最新价", "IOPV实时估值", "基金折价率", "涨跌额", "涨跌幅", 
                    "成交量", "成交额", "开盘价", "最高价", "最低价", "昨收", "换手率", 
                    "量比", "委比", "外盘", "内盘",
                    "主力净流入-净额", "主力净流入-净占比", 
                    "超大单净流入-净额", "超大单净流入-净占比",
                    "大单净流入-净额", "大单净流入-净占比", 
                    "中单净流入-净额", "中单净流入-净占比",
                    "小单净流入-净额", "小单净流入-净占比",
                    "现手", "买一", "卖一",
                    "最新份额", "流通市值", "总市值",
                    "数据日期", "更新时间"
                ],
            },
            {
                "name": "fund_etf_spot_ths",
                "display_name": "ETF基金实时行情-同花顺",
                "description": "同花顺-ETF实时行情数据，包括净值、增长率、申赎状态等",
                "route": "/funds/collections/fund_etf_spot_ths",
                "fields": ["序号", "基金代码", "基金名称", "当前-单位净值", "当前-累计净值", "前一日-单位净值", "前一日-累计净值", "增长值", "增长率", "赎回状态", "申购状态", "最新-交易日", "最新-单位净值", "最新-累计净值", "基金类型", "查询日期"],
            },
            {
                "name": "fund_lof_spot_em",
                "display_name": "LOF基金实时行情-东财",
                "description": "东方财富网-LOF实时行情数据，包括最新价、涨跌幅、成交量、市值等",
                "route": "/funds/collections/fund_lof_spot_em",
                "fields": ["代码", "名称", "最新价", "涨跌额", "涨跌幅", "成交量", "成交额", "开盘价", "最高价", "最低价", "昨收", "换手率", "流通市值", "总市值", "数据日期"],
            },
            {
                "name": "fund_spot_sina",
                "display_name": "基金实时行情-新浪",
                "description": "新浪财经-基金实时行情数据，支持封闭式基金、ETF基金、LOF基金三种类型",
                "route": "/funds/collections/fund_spot_sina",
                "fields": ["代码", "名称", "最新价", "涨跌额", "涨跌幅", "买入", "卖出", "昨收", "今开", "最高", "最低", "成交量", "成交额", "基金类型", "数据日期"],
            },
            {
                "name": "fund_etf_hist_min_em",
                "display_name": "ETF基金分时行情-东财",
                "description": "东方财富网-ETF 分时行情数据，支持按代码、时间周期、复权方式查询近期分钟级行情",
                "route": "/funds/collections/fund_etf_hist_min_em",
                "fields": [
                    "代码",
                    "时间",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "成交量",
                    "成交额",
                    "涨跌幅",
                    "涨跌额",
                    "振幅",
                    "换手率",
                    "period",
                    "adjust",
                ],
            },
            {
                "name": "fund_lof_hist_min_em",
                "display_name": "LOF基金分时行情-东财",
                "description": "东方财富网-LOF 分时行情数据，支持按代码、时间周期、复权方式查询近期分钟级行情",
                "route": "/funds/collections/fund_lof_hist_min_em",
                "fields": [
                    "代码",
                    "时间",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "成交量",
                    "成交额",
                    "涨跌幅",
                    "涨跌额",
                    "振幅",
                    "换手率",
                    "period",
                    "adjust",
                ],
            },
            {
                "name": "fund_etf_hist_em",
                "display_name": "ETF基金历史行情-东财",
                "description": "东方财富网-ETF 历史行情数据，支持按代码、周期（日/周/月）、复权方式查询历史K线数据",
                "route": "/funds/collections/fund_etf_hist_em",
                "fields": [
                    "代码",
                    "日期",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "成交量",
                    "成交额",
                    "振幅",
                    "涨跌幅",
                    "涨跌额",
                    "换手率",
                    "period",
                    "adjust",
                ],
            },
            {
                "name": "fund_lof_hist_em",
                "display_name": "LOF基金历史行情-东财",
                "description": "东方财富网-LOF 历史行情数据，支持按代码、周期（日/周/月）、复权方式查询历史K线数据",
                "route": "/funds/collections/fund_lof_hist_em",
                "fields": [
                    "代码",
                    "日期",
                    "开盘",
                    "收盘",
                    "最高",
                    "最低",
                    "成交量",
                    "成交额",
                    "振幅",
                    "涨跌幅",
                    "涨跌额",
                    "换手率",
                    "period",
                    "adjust",
                ],
            },
            {
                "name": "fund_hist_sina",
                "display_name": "基金历史行情-新浪",
                "description": "新浪财经-基金行情日频率数据，包含开盘、收盘、最高、最低、成交量等字段",
                "route": "/funds/collections/fund_hist_sina",
                "fields": [
                    "code",
                    "date",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                ],
            },
            {
                "name": "fund_open_fund_daily_em",
                "display_name": "开放式基金实时行情-东方财富",
                "description": "东方财富网-天天基金网-基金数据，每个交易日 16:00-23:00 更新当日最新开放式基金净值数据",
                "route": "/funds/collections/fund_open_fund_daily_em",
                "fields": [
                    "fund_code",
                    "fund_name",
                    "date",
                    "unit_net_value",
                    "cumulative_net_value",
                    "prev_unit_net_value",
                    "prev_cumulative_net_value",
                    "daily_growth_value",
                    "daily_growth_rate",
                    "purchase_status",
                    "redemption_status",
                    "fee",
                ],
            },
            {
                "name": "fund_open_fund_info_em",
                "display_name": "开放式基金历史行情-东方财富",
                "description": "东方财富网-天天基金网-基金历史数据，支持7个指标：单位净值走势、累计净值走势、累计收益率走势、同类排名走势、同类排名百分比、分红送配详情、拆分详情",
                "route": "/funds/collections/fund_open_fund_info_em",
                "fields": [
                    "fund_code",
                    "indicator",
                    "date",
                    "单位净值",
                    "累计净值",
                    "日增长率",
                    "累计收益率",
                    "同类型排名-每日近三月排名",
                    "总排名-每日近三月排名",
                    "同类型排名-每日近3月收益排名百分比",
                ],
            },
            {
                "name": "fund_money_fund_daily_em",
                "display_name": "货币型基金实时行情-东方财富",
                "description": "东方财富网-天天基金网-货币型基金收益，每个交易日 16:00-23:00 更新当日最新数据",
                "route": "/funds/collections/fund_money_fund_daily_em",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "日期",
                    "每万份收益",
                    "7日年化收益率",
                    "单位净值",
                    "前一日万份收益",
                    "前一日7日年化",
                    "前一日净值",
                    "日增长",
                    "成立日期",
                    "基金经理",
                    "手续费",
                    "申购状态",
                ],
            },
            {
                "name": "fund_money_fund_info_em",
                "display_name": "货币型基金历史行情-东方财富",
                "description": "东方财富网-天天基金网-货币型基金历史净值数据",
                "route": "/funds/collections/fund_money_fund_info_em",
                "fields": [
                    "基金代码",
                    "日期",
                    "每万份收益",
                    "7日年化收益率",
                    "申购状态",
                    "赎回状态",
                ],
            },
            {
                "name": "fund_financial_fund_daily_em",
                "display_name": "理财型基金实时行情-东方财富",
                "description": "东方财富网-天天基金网-理财型基金实时数据，每个交易日 16:00-23:00 更新",
                "route": "/funds/collections/fund_financial_fund_daily_em",
                "fields": [
                    "fund_code",
                    "fund_name",
                    "date",
                    "last_period_annual_yield",
                    "current_daily_profit_per_10k",
                    "current_7day_annual_yield",
                    "prev_daily_profit_per_10k",
                    "prev_7day_annual_yield",
                    "closed_period",
                    "purchase_status",
                ],
            },
            {
                "name": "fund_financial_fund_info_em",
                "display_name": "理财型基金历史行情-东方财富",
                "description": "东方财富网-天天基金网-理财型基金历史净值数据",
                "route": "/funds/collections/fund_financial_fund_info_em",
                "fields": [
                    "基金代码",
                    "日期",
                    "单位净值",
                    "累计净值",
                    "日增长率",
                    "申购状态",
                    "赎回状态",
                    "分红送配",
                ],
            },
            {
                "name": "fund_graded_fund_daily_em",
                "display_name": "分级基金实时数据-东方财富",
                "description": "东方财富网-天天基金网-分级基金实时数据，每个交易日 16:00-23:00 更新",
                "route": "/funds/collections/fund_graded_fund_daily_em",
                "fields": [
                    "fund_code",
                    "fund_name",
                    "date",
                    "unit_net_value",
                    "accumulative_net_value",
                    "prev_unit_net_value",
                    "prev_accumulative_net_value",
                    "daily_growth_value",
                    "daily_growth_rate",
                    "market_price",
                    "discount_rate",
                    "fee",
                ],
            },
            {
                "name": "fund_graded_fund_info_em",
                "display_name": "分级基金历史数据-东方财富",
                "description": "东方财富网-天天基金网-分级基金历史净值数据",
                "route": "/funds/collections/fund_graded_fund_info_em",
                "fields": [
                    "fund_code",
                    "date",
                    "净值日期",
                    "单位净值",
                    "累计净值",
                    "日增长率",
                    "申购状态",
                    "赎回状态",
                ],
            },
            {
                "name": "fund_etf_fund_daily_em",
                "display_name": "场内交易基金实时行情-东方财富",
                "description": "东方财富网-天天基金网-场内交易基金实时数据，每个交易日 16:00-23:00 更新",
                "route": "/funds/collections/fund_etf_fund_daily_em",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "类型",
                    "日期",
                    "单位净值",
                    "累计净值",
                    "增长值",
                    "增长率",
                    "市价",
                    "折价率",
                ],
            },
            {
                "name": "fund_hk_hist_em",
                "display_name": "香港基金-历史数据",
                "description": "东方财富网-天天基金网-香港基金-历史净值明细和分红送配详情",
                "route": "/funds/collections/fund_hk_hist_em",
                "fields": [
                    "code",
                    "symbol",
                    "date",
                    "净值日期",
                    "单位净值",
                    "日增长值",
                    "日增长率",
                    "单位",
                    "年份",
                    "权益登记日",
                    "除息日",
                    "分红发放日",
                    "分红金额",
                ],
            },
            {
                "name": "fund_etf_fund_info_em",
                "display_name": "场内交易基金-历史行情",
                "description": "东方财富网-天天基金网-场内交易基金-历史净值数据",
                "route": "/funds/collections/fund_etf_fund_info_em",
                "fields": [
                    "基金代码",
                    "日期",
                    "单位净值",
                    "累计净值",
                    "日增长率",
                    "申购状态",
                    "赎回状态",
                ],
            },
            {
                "name": "fund_etf_dividend_sina",
                "display_name": "基金累计分红-新浪",
                "description": "新浪财经-ETF基金累计分红数据，包含除权除息日、累计分红金额",
                "route": "/funds/collections/fund_etf_dividend_sina",
                "fields": [
                    "fund_code",
                    "code",
                    "日期",
                    "累计分红",
                    "source",
                    "updated_at",
                ],
            },
            {
                "name": "fund_fh_em",
                "display_name": "基金分红-东财",
                "description": "东方财富网-天天基金网-基金数据-分红送配-基金分红，包含权益登记日、除息日期、分红金额等",
                "route": "/funds/collections/fund_fh_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "权益登记日",
                    "除息日期",
                    "分红",
                    "分红发放日",
                    "source",
                    "updated_at",
                ],
            },
            {
                "name": "fund_cf_em",
                "display_name": "基金拆分-东方财富",
                "description": "东方财富网-天天基金网-基金数据-分红送配-基金拆分，包含拆分折算日、拆分类型、拆分折算比例等",
                "route": "/funds/collections/fund_cf_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "拆分折算日",
                    "拆分类型",
                    "拆分折算",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_fh_rank_em",
                "display_name": "基金分红排行-东方财富",
                "description": "东方财富网-天天基金网-基金数据-分红送配-基金分红排行，包含累计分红、累计次数、成立日期等",
                "route": "/funds/collections/fund_fh_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "累计分红",
                    "累计次数",
                    "成立日期",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_open_fund_rank_em",
                "display_name": "开放式基金排行-东方财富",
                "description": "东方财富网-数据中心-开放式基金排行，支持按类型筛选(全部/股票型/混合型/债券型/指数型/QDII/FOF)",
                "route": "/funds/collections/fund_open_fund_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "日期",
                    "单位净值",
                    "累计净值",
                    "日增长率",
                    "近1周",
                    "近1月",
                    "近3月",
                    "近6月",
                    "近1年",
                    "近2年",
                    "近3年",
                    "今年来",
                    "成立来",
                    "自定义",
                    "手续费",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_exchange_rank_em",
                "display_name": "场内交易基金排行-东财",
                "description": "东方财富网-数据中心-场内交易基金排行榜，每个交易日17点后更新",
                "route": "/funds/collections/fund_exchange_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "类型",
                    "日期",
                    "单位净值",
                    "累计净值",
                    "近1周",
                    "近1月",
                    "近3月",
                    "近6月",
                    "近1年",
                    "近2年",
                    "近3年",
                    "今年来",
                    "成立来",
                    "成立日期",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_money_rank_em",
                "display_name": "货币型基金排行-东财",
                "description": "东方财富网-数据中心-货币型基金排行，每个交易日17点后更新",
                "route": "/funds/collections/fund_money_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "日期",
                    "万份收益",
                    "年化收益率7日",
                    "年化收益率14日",
                    "年化收益率28日",
                    "近1月",
                    "近3月",
                    "近6月",
                    "近1年",
                    "近2年",
                    "近3年",
                    "近5年",
                    "今年来",
                    "成立来",
                    "手续费",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_lcx_rank_em",
                "display_name": "理财基金排行-东财",
                "description": "东方财富网-数据中心-理财基金排行（注：目标网站暂无数据）",
                "route": "/funds/collections/fund_lcx_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "日期",
                    "万份收益",
                    "年化收益率7日",
                    "年化收益率14日",
                    "年化收益率28日",
                    "近1周",
                    "近1月",
                    "近3月",
                    "近6月",
                    "今年来",
                    "成立来",
                    "可购买",
                    "手续费",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_hk_rank_em",
                "display_name": "香港基金排行-东财",
                "description": "东方财富网-数据中心-基金排行-香港基金排行",
                "route": "/funds/collections/fund_hk_rank_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金简称",
                    "币种",
                    "日期",
                    "单位净值",
                    "日增长率",
                    "近1周",
                    "近1月",
                    "近3月",
                    "近6月",
                    "近1年",
                    "近2年",
                    "近3年",
                    "今年来",
                    "成立来",
                    "可购买",
                    "香港基金代码",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_individual_achievement_xq",
                "display_name": "基金业绩-雪球",
                "description": "雪球基金-基金详情-基金业绩-详情（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_individual_achievement_xq",
                "fields": [
                    "业绩类型",
                    "周期",
                    "本产品区间收益",
                    "本产品最大回撒",
                    "周期收益同类排名",
                    "基金代码",
                    "code",
                    "performance_type",
                    "period",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_value_estimation_em",
                "display_name": "净值估算-东财",
                "description": "东方财富网-数据中心-净值估算（支持按基金类型过滤）",
                "route": "/funds/collections/fund_value_estimation_em",
                "fields": [
                    "序号",
                    "基金代码",
                    "基金名称",
                    "估算数据-估算值",
                    "估算数据-估算增长率",
                    "公布数据-单位净值",
                    "公布数据-日增长率",
                    "估算偏差",
                    "单位净值",
                    "日期",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_individual_analysis_xq",
                "display_name": "基金数据分析-雪球",
                "description": "雪球基金-基金详情-数据分析（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_individual_analysis_xq",
                "fields": [
                    "周期",
                    "较同类风险收益比",
                    "较同类抗风险波动",
                    "年化波动率",
                    "年化夏普比率",
                    "最大回撤",
                    "基金代码",
                    "code",
                    "period",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_individual_profit_probability_xq",
                "display_name": "基金盈利概率-雪球",
                "description": "雪球基金-基金详情-盈利概率（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_individual_profit_probability_xq",
                "fields": [
                    "持有时长",
                    "盈利概率",
                    "平均收益",
                    "基金代码",
                    "日期",
                    "code",
                    "date",
                    "holding_period",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_individual_detail_hold_xq",
                "display_name": "基金持仓资产比例-雪球",
                "description": "雪球基金-基金详情-持仓资产比例（需要基金代码和日期，支持单个/批量更新）",
                "route": "/funds/collections/fund_individual_detail_hold_xq",
                "fields": [
                    "基金代码",
                    "日期",
                    "持仓信息",
                    "数据源",
                    "接口名称",
                    "更新时间",
                ],
            },
            {
                "name": "fund_overview_em",
                "display_name": "基金基本概况-东财",
                "description": "东方财富网-数据中心-基金基本概况（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_overview_em",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "基金类型",
                    "发行日期",
                    "成立日期",
                    "基金规模",
                    "基金管理人",
                    "基金托管人",
                    "基金经理",
                    "管理费率",
                    "托管费率",
                    "业绩比较基准",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_fee_em",
                "display_name": "基金交易费率-东财",
                "description": "东方财富网-数据中心-基金交易费率（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_fee_em",
                "fields": [
                    "基金代码",
                    "费用类型",
                    "条件",
                    "费率",
                    "优惠费率",
                    "code",
                    "fee_type",
                    "condition",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_individual_detail_info_xq",
                "display_name": "基金交易规则-雪球",
                "description": "雪球基金-基金详情-交易规则（需要基金代码，支持单个/批量更新）",
                "route": "/funds/collections/fund_individual_detail_info_xq",
                "fields": [
                    "基金代码",
                    "费用类型",
                    "规则说明",
                    "最小金额",
                    "最大金额",
                    "交易确认",
                    "到账时间",
                    "code",
                    "fee_type",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_portfolio_hold_em",
                "display_name": "基金持仓-东财",
                "description": "东方财富网-数据中心-基金持仓（需要基金代码和日期，支持单个/批量更新）",
                "route": "/funds/collections/fund_portfolio_hold_em",
                "fields": [
                    "基金代码",
                    "股票代码",
                    "股票名称",
                    "季度",
                    "持仓占比",
                    "持仓数量",
                    "持仓市值",
                    "数据源",
                    "接口名称",
                    "更新时间",
                ],
            },
            {
                "name": "fund_portfolio_bond_hold_em",
                "display_name": "债券持仓-东财",
                "description": "东方财富网-数据中心-债券持仓（需要基金代码和日期，支持单个/批量更新）",
                "route": "/funds/collections/fund_portfolio_bond_hold_em",
                "fields": [
                    "基金代码",
                    "债券代码",
                    "债券名称",
                    "季度",
                    "持仓占比",
                    "持仓数量",
                    "持仓市值",
                    "code",
                    "bond_code",
                    "quarter",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_portfolio_industry_allocation_em",
                "display_name": "行业配置-东财",
                "description": "东方财富网-数据中心-行业配置（需要基金代码和日期，支持单个/批量更新）",
                "route": "/funds/collections/fund_portfolio_industry_allocation_em",
                "fields": [
                    "基金代码",
                    "行业类别",
                    "截止时间",
                    "占净值比例",
                    "code",
                    "industry",
                    "end_date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_portfolio_change_em",
                "display_name": "重大变动-东财",
                "description": "东方财富网-数据中心-重大变动（需要基金代码和年份，支持单个/批量更新）",
                "route": "/funds/collections/fund_portfolio_change_em",
                "fields": [
                    "序号",
                    "股票代码",
                    "股票名称",
                    "本期累计买入金额",
                    "占期初基金资产净值比例",
                    "季度",
                    "基金代码",
                    "code",
                    "stock_code",
                    "quarter",
                    "indicator_type",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_rating_all_em",
                "display_name": "基金评级总汇-东财",
                "description": "东方财富网-基金评级-基金评级总汇（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_rating_all_em",
                "fields": [
                    "代码",
                    "简称",
                    "基金经理",
                    "基金公司",
                    "5星评级家数",
                    "上海证券",
                    "招商证券",
                    "济安金信",
                    "手续费",
                    "类型",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_rating_sh_em",
                "display_name": "上海证券评级-东财",
                "description": "东方财富网-基金评级-上海证券评级（需要日期参数YYYYMMDD）",
                "route": "/funds/collections/fund_rating_sh_em",
                "fields": [
                    "代码",
                    "简称",
                    "基金经理",
                    "基金公司",
                    "3年期评级-3年评级",
                    "3年期评级-较上期",
                    "5年期评级-5年评级",
                    "5年期评级-较上期",
                    "单位净值",
                    "日期",
                    "日增长率",
                    "近1年涨幅",
                    "近3年涨幅",
                    "近5年涨幅",
                    "手续费",
                    "类型",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_rating_zs_em",
                "display_name": "招商证券评级-东财",
                "description": "东方财富网-基金评级-招商证券评级（需要日期参数YYYYMMDD）",
                "route": "/funds/collections/fund_rating_zs_em",
                "fields": [
                    "代码",
                    "简称",
                    "基金经理",
                    "基金公司",
                    "3年期评级-3年评级",
                    "3年期评级-较上期",
                    "5年期评级-5年评级",
                    "5年期评级-较上期",
                    "单位净值",
                    "日期",
                    "日增长率",
                    "近1年涨幅",
                    "近3年涨幅",
                    "近5年涨幅",
                    "手续费",
                    "类型",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_rating_ja_em",
                "display_name": "济安金信评级-东财",
                "description": "东方财富网-基金评级-济安金信评级（需要日期参数YYYYMMDD）",
                "route": "/funds/collections/fund_rating_ja_em",
                "fields": [
                    "代码",
                    "简称",
                    "基金经理",
                    "基金公司",
                    "3年期评级-3年评级",
                    "3年期评级-较上期",
                    "5年期评级-5年评级",
                    "5年期评级-较上期",
                    "单位净值",
                    "日期",
                    "日增长率",
                    "近1年涨幅",
                    "近3年涨幅",
                    "近5年涨幅",
                    "手续费",
                    "类型",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_manager_em",
                "display_name": "基金经理-东财",
                "description": "东方财富网-基金数据-基金经理大全（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_manager_em",
                "fields": [
                    "序号",
                    "姓名",
                    "所属公司",
                    "现任基金代码",
                    "现任基金",
                    "累计从业时间",
                    "现任基金资产总规模",
                    "现任基金最佳回报",
                    "name",
                    "fund_codes",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_new_found_em",
                "display_name": "新发基金-东财",
                "description": "东方财富网-基金数据-新发基金（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_new_found_em",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "发行公司",
                    "基金类型",
                    "集中认购期",
                    "募集份额",
                    "成立日期",
                    "基金经理",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_scale_open_sina",
                "display_name": "开放式基金规模-新浪",
                "description": "新浪财经-基金数据-开放式基金规模（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_scale_open_sina",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "管理公司",
                    "成立日期",
                    "最新份额",
                    "最新规模",
                    "汇率",
                    "更新日期",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_scale_close_sina",
                "display_name": "封闭式基金规模-新浪",
                "description": "新浪财经-基金数据-封闭式基金规模（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_scale_close_sina",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "管理公司",
                    "成立日期",
                    "最新份额",
                    "最新规模",
                    "汇率",
                    "更新日期",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_scale_structured_sina",
                "display_name": "分级子基金规模-新浪",
                "description": "新浪财经-基金数据-分级子基金规模（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_scale_structured_sina",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "管理公司",
                    "成立日期",
                    "最新份额",
                    "最新规模",
                    "汇率",
                    "更新日期",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_aum_em",
                "display_name": "基金规模详情-东财",
                "description": "东方财富网-基金数据-基金公司管理规模（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_aum_em",
                "fields": [
                    "序号",
                    "基金公司",
                    "总规模",
                    "股票型",
                    "混合型",
                    "债券型",
                    "指数型",
                    "QDII",
                    "货币型",
                    "更新日期",
                    "company",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_aum_trend_em",
                "display_name": "基金规模走势-东财",
                "description": "东方财富网-基金数据-基金规模走势（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_aum_trend_em",
                "fields": [
                    "date",
                    "total_aum",
                    "equity_aum",
                    "hybrid_aum",
                    "bond_aum",
                    "index_aum",
                    "qdii_aum",
                    "money_aum",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_aum_hist_em",
                "display_name": "基金公司历年管理规模-东财",
                "description": "东方财富网-基金数据-基金公司历年管理规模（无需参数，支持更新所有）",
                "route": "/funds/collections/fund_aum_hist_em",
                "fields": [
                    "序号",
                    "基金公司",
                    "总规模",
                    "股票型",
                    "混合型",
                    "债券型",
                    "指数型",
                    "QDII",
                    "货币型",
                    "更新日期",
                    "company",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "reits_realtime_em",
                "display_name": "REITs实时行情-东财",
                "description": "东方财富网-行情中心-REITs-沪深 REITs-实时行情（无需参数，支持更新所有）",
                "route": "/funds/collections/reits_realtime_em",
                "fields": [
                    "序号",
                    "代码",
                    "名称",
                    "最新价",
                    "涨跌额",
                    "涨跌幅",
                    "成交量",
                    "成交额",
                    "开盘价",
                    "最高价",
                    "最低价",
                    "昨收",
                    "code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "reits_hist_em",
                "display_name": "REITs历史行情-东财",
                "description": "东方财富网-行情中心-REITs-沪深 REITs-历史行情（需code参数，不传则更新所有）",
                "route": "/funds/collections/reits_hist_em",
                "fields": [
                    "date",
                    "open",
                    "close",
                    "high",
                    "low",
                    "volume",
                    "amount",
                    "adjust",
                    "code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_report_stock_cninfo",
                "display_name": "基金重仓股-巨潮",
                "description": "巨潮资讯-基金数据-基金重仓股（需date参数，YYYYMMDD格式，默认最近季度）",
                "route": "/funds/collections/fund_report_stock_cninfo",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "股票代码",
                    "股票名称",
                    "持仓比例",
                    "持仓股数",
                    "持仓市值",
                    "报告期",
                    "fund_code",
                    "stock_code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_report_industry_allocation_cninfo",
                "display_name": "基金行业配置-巨潮",
                "description": "巨潮资讯-基金数据-基金行业配置（需date参数，YYYYMMDD格式，默认最近季度）",
                "route": "/funds/collections/fund_report_industry_allocation_cninfo",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "行业名称",
                    "行业编码",
                    "市值",
                    "市值占净值比",
                    "报告期",
                    "fund_code",
                    "industry_name",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_report_asset_allocation_cninfo",
                "display_name": "基金资产配置-巨潮",
                "description": "巨潮资讯-基金数据-基金资产配置（需date参数，YYYYMMDD格式，默认最近季度）",
                "route": "/funds/collections/fund_report_asset_allocation_cninfo",
                "fields": [
                    "基金代码",
                    "基金简称",
                    "股票占净比",
                    "债券占净比",
                    "现金占净比",
                    "净资产",
                    "报告期",
                    "fund_code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_scale_change_em",
                "display_name": "规模变动-东财",
                "description": "东方财富网-基金数据-规模变动（需code参数）",
                "route": "/funds/collections/fund_scale_change_em",
                "fields": [
                    "截止日期",
                    "净资产",
                    "期间申购",
                    "期间赎回",
                    "期末总份额",
                    "fund_code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_hold_structure_em",
                "display_name": "持有人结构-东财",
                "description": "东方财富网-基金数据-持有人结构（需code参数）",
                "route": "/funds/collections/fund_hold_structure_em",
                "fields": [
                    "截止日期",
                    "机构持有比例",
                    "个人持有比例",
                    "内部持有比例",
                    "总份额",
                    "fund_code",
                    "date",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_stock_position_lg",
                "display_name": "股票型基金仓位-乐咕乐股",
                "description": "乐咕乐股-基金数据-股票型基金仓位（无参数）",
                "route": "/funds/collections/fund_stock_position_lg",
                "fields": [
                    "date",
                    "仓位",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_balance_position_lg",
                "display_name": "平衡混合型基金仓位-乐咕乐股",
                "description": "乐咕乐股-基金数据-平衡混合型基金仓位（无参数）",
                "route": "/funds/collections/fund_balance_position_lg",
                "fields": [
                    "date",
                    "仓位",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_linghuo_position_lg",
                "display_name": "灵活配置型基金仓位-乐咕乐股",
                "description": "乐咕乐股-基金数据-灵活配置型基金仓位（无参数）",
                "route": "/funds/collections/fund_linghuo_position_lg",
                "fields": [
                    "date",
                    "仓位",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_announcement_dividend_em",
                "display_name": "基金公告分红配送-东财",
                "description": "东方财富网-基金数据-公告-分红配送（无参数）",
                "route": "/funds/collections/fund_announcement_dividend_em",
                "fields": [
                    "date",
                    "title",
                    "fund_code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_announcement_report_em",
                "display_name": "基金公告定期报告-东财",
                "description": "东方财富网-基金数据-公告-定期报告（无参数）",
                "route": "/funds/collections/fund_announcement_report_em",
                "fields": [
                    "date",
                    "title",
                    "fund_code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
            {
                "name": "fund_announcement_personnel_em",
                "display_name": "基金公告人事调整-东财",
                "description": "东方财富网-基金数据-公告-人事调整（无参数）",
                "route": "/funds/collections/fund_announcement_personnel_em",
                "fields": [
                    "date",
                    "title",
                    "fund_code",
                    "source",
                    "endpoint",
                    "updated_at",
                ],
            },
        ]
        
        return {
            "success": True,
            "data": collections
        }
    except Exception as e:
        logger.error(f"获取基金集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/update-config")
async def get_fund_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定基金集合的更新配置"""
    try:
        config = get_collection_update_config(collection_name)
        return {
            "success": True,
            "data": config
        }
    except Exception as e:
        logger.error(f"获取基金集合更新配置失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}")
async def get_fund_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量，默认50"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    tracking_target: Optional[str] = Query(None, description="跟踪标的筛选"),
    tracking_method: Optional[str] = Query(None, description="跟踪方式筛选"),
    fund_company: Optional[str] = Query(None, description="基金公司筛选"),
    current_user: dict = Depends(get_current_user),
):
    """获取指定基金集合的数据（分页）"""
    db = get_mongo_db()
    
    # 集合映射
    collection_map = {
        "fund_name_em": db.get_collection("fund_name_em"),
        "fund_basic_info": db.get_collection("fund_basic_info"),
        "fund_info_index_em": db.get_collection("fund_info_index_em"),
        "fund_net_value": db.get_collection("fund_net_value"),
        "fund_ranking": db.get_collection("fund_ranking"),
        "fund_purchase_status": db.get_collection("fund_purchase_status"),
        "fund_etf_spot_em": db.get_collection("fund_etf_spot_em"),
        "fund_etf_spot_ths": db.get_collection("fund_etf_spot_ths"),
        "fund_lof_spot_em": db.get_collection("fund_lof_spot_em"),
        "fund_spot_sina": db.get_collection("fund_spot_sina"),
        "fund_etf_hist_min_em": db.get_collection("fund_etf_hist_min_em"),
        "fund_lof_hist_min_em": db.get_collection("fund_lof_hist_min_em"),
        "fund_etf_hist_em": db.get_collection("fund_etf_hist_em"),
        "fund_lof_hist_em": db.get_collection("fund_lof_hist_em"),
        "fund_hist_sina": db.get_collection("fund_hist_sina"),
        "fund_open_fund_daily_em": db.get_collection("fund_open_fund_daily_em"),
        "fund_open_fund_info_em": db.get_collection("fund_open_fund_info_em"),
        "fund_money_fund_daily_em": db.get_collection("fund_money_fund_daily_em"),
        "fund_money_fund_info_em": db.get_collection("fund_money_fund_info_em"),
        "fund_financial_fund_daily_em": db.get_collection("fund_financial_fund_daily_em"),
        "fund_financial_fund_info_em": db.get_collection("fund_financial_fund_info_em"),
        "fund_graded_fund_daily_em": db.get_collection("fund_graded_fund_daily_em"),
        "fund_graded_fund_info_em": db.get_collection("fund_graded_fund_info_em"),
        "fund_etf_fund_daily_em": db.get_collection("fund_etf_fund_daily_em"),
        "fund_hk_hist_em": db.get_collection("fund_hk_hist_em"),
        "fund_etf_fund_info_em": db.get_collection("fund_etf_fund_info_em"),
        "fund_etf_dividend_sina": db.get_collection("fund_etf_dividend_sina"),
        "fund_fh_em": db.get_collection("fund_fh_em"),
        "fund_cf_em": db.get_collection("fund_cf_em"),
        "fund_fh_rank_em": db.get_collection("fund_fh_rank_em"),
        "fund_open_fund_rank_em": db.get_collection("fund_open_fund_rank_em"),
        "fund_exchange_rank_em": db.get_collection("fund_exchange_rank_em"),
        "fund_money_rank_em": db.get_collection("fund_money_rank_em"),
        "fund_lcx_rank_em": db.get_collection("fund_lcx_rank_em"),
        "fund_hk_rank_em": db.get_collection("fund_hk_rank_em"),
        "fund_individual_achievement_xq": db.get_collection("fund_individual_achievement_xq"),
        "fund_value_estimation_em": db.get_collection("fund_value_estimation_em"),
        "fund_individual_analysis_xq": db.get_collection("fund_individual_analysis_xq"),
        "fund_individual_profit_probability_xq": db.get_collection("fund_individual_profit_probability_xq"),
        "fund_individual_detail_hold_xq": db.get_collection("fund_individual_detail_hold_xq"),
        "fund_overview_em": db.get_collection("fund_overview_em"),
        "fund_fee_em": db.get_collection("fund_fee_em"),
        "fund_individual_detail_info_xq": db.get_collection("fund_individual_detail_info_xq"),
        "fund_portfolio_hold_em": db.get_collection("fund_portfolio_hold_em"),
        "fund_portfolio_bond_hold_em": db.get_collection("fund_portfolio_bond_hold_em"),
        "fund_portfolio_industry_allocation_em": db.get_collection("fund_portfolio_industry_allocation_em"),
        "fund_portfolio_change_em": db.get_collection("fund_portfolio_change_em"),
        "fund_rating_all_em": db.get_collection("fund_rating_all_em"),
        "fund_rating_sh_em": db.get_collection("fund_rating_sh_em"),
        "fund_rating_zs_em": db.get_collection("fund_rating_zs_em"),
        "fund_rating_ja_em": db.get_collection("fund_rating_ja_em"),
        "fund_manager_em": db.get_collection("fund_manager_em"),
        "fund_new_found_em": db.get_collection("fund_new_found_em"),
        "fund_scale_open_sina": db.get_collection("fund_scale_open_sina"),
        "fund_scale_close_sina": db.get_collection("fund_scale_close_sina"),
        "fund_scale_structured_sina": db.get_collection("fund_scale_structured_sina"),
        "fund_aum_em": db.get_collection("fund_aum_em"),
        "fund_aum_trend_em": db.get_collection("fund_aum_trend_em"),
        "fund_aum_hist_em": db.get_collection("fund_aum_hist_em"),
        "reits_realtime_em": db.get_collection("reits_realtime_em"),
        "reits_hist_em": db.get_collection("reits_hist_em"),
        "fund_report_stock_cninfo": db.get_collection("fund_report_stock_cninfo"),
        "fund_report_industry_allocation_cninfo": db.get_collection("fund_report_industry_allocation_cninfo"),
        "fund_report_asset_allocation_cninfo": db.get_collection("fund_report_asset_allocation_cninfo"),
        "fund_scale_change_em": db.get_collection("fund_scale_change_em"),
        "fund_hold_structure_em": db.get_collection("fund_hold_structure_em"),
        "fund_stock_position_lg": db.get_collection("fund_stock_position_lg"),
        "fund_balance_position_lg": db.get_collection("fund_balance_position_lg"),
        "fund_linghuo_position_lg": db.get_collection("fund_linghuo_position_lg"),
        "fund_announcement_dividend_em": db.get_collection("fund_announcement_dividend_em"),
        "fund_announcement_report_em": db.get_collection("fund_announcement_report_em"),
        "fund_announcement_personnel_em": db.get_collection("fund_announcement_personnel_em"),
    }
    
    collection = collection_map.get(collection_name)
    if collection is None:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    
    try:
        # 构建查询条件
        query = {}
        if filter_field and filter_value:
            filter_field_stripped = filter_field.strip()
            filter_value_stripped = filter_value.strip()
            if filter_field_stripped and filter_value_stripped:
                if filter_field_stripped in ["code", "name"]:
                    query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                else:
                    query[filter_field_stripped] = filter_value_stripped
        
        # 添加指数型基金特定筛选
        if collection_name == "fund_info_index_em":
            if tracking_target and tracking_target != "全部":
                query["跟踪标的"] = tracking_target
            if tracking_method and tracking_method != "全部":
                query["跟踪方式"] = tracking_method
                
            # 基金公司筛选 (关联查询)
            if fund_company and fund_company != "全部":
                basic_info_col = db.get_collection("fund_basic_info")
                # 查找该公司的所有基金代码
                # 尝试匹配 "基金公司" 字段
                company_funds = await basic_info_col.find(
                    {"基金公司": fund_company}, 
                    {"code": 1, "基金代码": 1}
                ).to_list(None)
                
                codes = []
                for doc in company_funds:
                    # 优先使用 code，其次 基金代码
                    if "code" in doc:
                        codes.append(doc["code"])
                    elif "基金代码" in doc:
                        codes.append(doc["基金代码"])
                
                if codes:
                    # fund_info_index_em 使用 "code" 或 "基金代码" ? 
                    # 根据之前的 edit，它使用 "code" 作为索引键，但原始数据里有 "基金代码"
                    # 让我们两个都查一下，或者使用 $in
                    # 如果 fund_info_index_em 已经规范化了 code 字段（在之前的 edit 中我们加了 code 字段）
                    query["code"] = {"$in": codes}
                else:
                    # 没有找到对应公司的基金
                    query["code"] = "IMPOSSIBLE_CODE"
        
        # 获取总数
        total = await collection.count_documents(query)
        
        # 构建排序
        sort_key = sort_by if sort_by else "_id"
        sort_direction = -1 if sort_dir == "desc" else 1
        
        # 分页查询
        skip = (page - 1) * page_size
        cursor = collection.find(query).sort(sort_key, sort_direction).skip(skip).limit(page_size)
        items = []
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)
        
        # 获取字段信息
        fields_info = []
        if items:
            sample = items[0]
            
            # 获取预定义的字段顺序
            defined_fields_order = _get_collection_fields_order(collection_name)
            
            # 构建字段信息字典
            fields_dict = {}
            for key, value in sample.items():
                if key != "_id":
                    field_type = type(value).__name__
                    if field_type == "int":
                        field_type = "整数"
                    elif field_type == "float":
                        field_type = "浮点数"
                    elif field_type == "bool":
                        field_type = "布尔值"
                    elif field_type == "list":
                        field_type = "列表"
                    elif field_type == "dict":
                        field_type = "对象"
                    else:
                        field_type = "字符串"
                    fields_dict[key] = {
                        "name": key,
                        "type": field_type,
                        "example": str(value)[:50] if value is not None else None,
                    }
            
            # 按预定义顺序排列字段
            if defined_fields_order:
                # 先添加预定义顺序的字段
                for field_name in defined_fields_order:
                    if field_name in fields_dict:
                        fields_info.append(fields_dict[field_name])
                        del fields_dict[field_name]
                # 再添加未在预定义列表中的字段（按原顺序）
                for field_info in fields_dict.values():
                    fields_info.append(field_info)
            else:
                # 如果没有预定义顺序，按原始顺序
                fields_info = list(fields_dict.values())
        
        return {
            "success": True,
            "data": {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "fields": fields_info,
            },
        }
    except Exception as e:
        logger.error(f"获取基金集合 {collection_name} 数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_fund_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取基金集合统计信息"""
    try:
        # 使用新的 FundRefreshService (V2) 统一获取集合概览
        from app.services.fund_refresh_service import FundRefreshService
        db = get_mongo_db()
        refresh_service = FundRefreshService(db)
        
        # 检查集合是否支持
        supported_collections = refresh_service.get_supported_collections()
        if collection_name not in supported_collections:
            return {"success": False, "error": f"集合 {collection_name} 不存在"}
        
        # 获取集合统计信息
        stats = await refresh_service.get_collection_overview(collection_name)
        stats["collection_name"] = collection_name
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取基金集合统计失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/companies")
async def get_fund_companies(current_user: dict = Depends(get_current_user)):
    """获取所有基金公司列表"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("fund_basic_info")
        companies = await collection.distinct("基金公司")
        # 过滤掉空值
        companies = [c for c in companies if c]
        companies.sort()
        return {"success": True, "data": companies}
    except Exception as e:
        logger.error(f"获取基金公司列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/search")
async def search_funds(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: dict = Depends(get_current_user),
):
    """搜索基金"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("fund_basic_info")
        
        # 按代码或名称搜索
        query = {
            "$or": [
                {"code": {"$regex": keyword, "$options": "i"}},
                {"name": {"$regex": keyword, "$options": "i"}},
            ]
        }
        
        cursor = collection.find(query).limit(20)
        results = []
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            results.append(doc)
        
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        logger.error(f"搜索基金失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/analysis/{fund_code}")
async def get_fund_analysis(
    fund_code: str,
    current_user: dict = Depends(get_current_user),
):
    """获取基金分析数据"""
    try:
        db = get_mongo_db()
        
        # 获取基金基础信息
        basic_info = await db.get_collection("fund_basic_info").find_one({"code": fund_code})
        
        if not basic_info:
            return {"success": False, "error": f"未找到基金 {fund_code}"}
        
        if "_id" in basic_info:
            basic_info["_id"] = str(basic_info["_id"])
        
        # 获取净值数据
        net_value_cursor = db.get_collection("fund_net_value").find(
            {"code": fund_code}
        ).sort("date", -1).limit(100)
        
        net_values = []
        async for doc in net_value_cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            net_values.append(doc)
        
        return {
            "success": True,
            "data": {
                "basic_info": basic_info,
                "net_values": net_values,
                "message": "基金分析功能正在开发中"
            }
        }
    except Exception as e:
        logger.error(f"获取基金分析失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/refresh")
async def refresh_fund_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    """刷新基金数据集合"""
    try:
        logger.info(f"[API refresh] 接收到刷新请求: collection={collection_name}, params={params}")
        db = get_mongo_db()
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"更新基金集合: {collection_name}"
        )
        
        # 在后台异步执行刷新任务
        async def do_refresh():
            try:
                refresh_service = FundRefreshService(db)
                await refresh_service.refresh_collection(collection_name, task_id, params)
            except Exception as e:
                logger.error(f"后台刷新任务失败: {e}", exc_info=True)
                # 确保任务状态被标记为失败
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_refresh)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"刷新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"刷新基金集合失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/refresh/status/{task_id}")
async def get_refresh_task_status(
    collection_name: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取刷新任务状态"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)
        
        if not task:
            return {"success": False, "error": "任务不存在"}
        
        return {
            "success": True,
            "data": task
        }
    except Exception as e:
        logger.error(f"获取任务状态失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/upload")
async def upload_fund_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金数据文件"""
    try:
        if not file.filename.endswith(('.csv', '.xls', '.xlsx')):
             return {"success": False, "error": "只支持CSV或Excel文件"}
             
        db = get_mongo_db()
        service = FundDataService(db)
        
        # Read file content
        content = await file.read()
        filename = file.filename
        
        result = await service.import_data_from_file(collection_name, content, filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传文件失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/sync")
async def sync_fund_data(
    collection_name: str,
    sync_config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """远程同步基金数据"""
    try:
        db = get_mongo_db()
        service = FundDataService(db)
        
        result = await service.sync_data_from_remote(collection_name, sync_config)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"远程同步失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.delete("/collections/{collection_name}/clear")
async def clear_fund_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空基金数据集合（统一使用通用清空方法）"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        # 统一调用通用清空方法
        deleted_count = await data_service.clear_fund_data(collection_name)
        
        return {
            "success": True,
            "data": {
                "deleted_count": deleted_count,
                "message": f"成功清空 {deleted_count} 条数据"
            }
        }
            
    except Exception as e:
        logger.error(f"清空基金集合失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_etf_dividend_sina/upload")
async def upload_fund_etf_dividend_sina(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金累计分红数据文件"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        content = await file.read()
        result = await data_service.import_fund_etf_dividend_sina_from_file(content, file.filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传基金累计分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_etf_dividend_sina/sync")
async def sync_fund_etf_dividend_sina(
    remote_host: str = Body(..., embed=True),
    batch_size: int = Body(5000, embed=True),
    remote_collection: str = Body(None, embed=True),
    remote_username: str = Body(None, embed=True),
    remote_password: str = Body(None, embed=True),
    remote_auth_source: str = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """从远程MongoDB同步基金累计分红数据"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        result = await data_service.sync_fund_etf_dividend_sina_from_remote(
            remote_host=remote_host,
            batch_size=batch_size,
            remote_collection=remote_collection,
            remote_username=remote_username,
            remote_password=remote_password,
            remote_auth_source=remote_auth_source,
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"同步基金累计分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_fh_em/upload")
async def upload_fund_fh_em(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传基金分红数据文件"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        content = await file.read()
        result = await data_service.import_fund_fh_em_from_file(content, file.filename)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"上传基金分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_fh_em/sync")
async def sync_fund_fh_em(
    remote_host: str = Body(..., embed=True),
    batch_size: int = Body(5000, embed=True),
    remote_collection: str = Body(None, embed=True),
    remote_username: str = Body(None, embed=True),
    remote_password: str = Body(None, embed=True),
    remote_auth_source: str = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """从远程MongoDB同步基金分红数据"""
    try:
        db = get_mongo_db()
        data_service = FundDataService(db)
        
        result = await data_service.sync_fund_fh_em_from_remote(
            remote_host=remote_host,
            batch_size=batch_size,
            remote_collection=remote_collection,
            remote_username=remote_username,
            remote_password=remote_password,
            remote_auth_source=remote_auth_source,
        )
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"同步基金分红数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 基金公告人事调整批量更新 API ====================

@router.post("/collections/fund_announcement_personnel_em/update/single")
async def update_single_fund_personnel(
    background_tasks: BackgroundTasks,
    fund_code: str = Body(..., embed=True),
    current_user: dict = Depends(get_current_user),
):
    """更新单个基金的公告人事调整数据"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_single_fund_personnel",
            description=f"更新基金 {fund_code} 公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_single_fund(task_id, fund_code)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_announcement_personnel_em/update/batch")
async def update_batch_fund_personnel(
    background_tasks: BackgroundTasks,
    fund_codes: List[str] = Body(..., embed=True),
    batch_size: int = Body(100, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """批量更新多个基金的公告人事调整数据"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_batch_fund_personnel",
            description=f"批量更新 {len(fund_codes)} 个基金的公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_batch_funds(task_id, fund_codes, batch_size)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"批量更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建批量更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/fund_announcement_personnel_em/update/incremental")
async def update_incremental_fund_personnel(
    background_tasks: BackgroundTasks,
    limit: int = Body(None, embed=True),
    current_user: dict = Depends(get_current_user),
):
    """增量更新：从fund_name_em获取基金代码并批量更新"""
    try:
        from app.services.fund_announcement_personnel_batch_service import FundAnnouncementPersonnelBatchService
        
        task_manager = get_task_manager()
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type="update_incremental_fund_personnel",
            description="增量更新基金公告人事调整数据"
        )
        
        # 在后台异步执行
        async def do_update():
            try:
                service = FundAnnouncementPersonnelBatchService(task_manager)
                await service.update_incremental(task_id, limit)
            except Exception as e:
                logger.error(f"后台更新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_update)
        
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"增量更新任务已创建"
            }
        }
    except Exception as e:
        logger.error(f"创建增量更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
