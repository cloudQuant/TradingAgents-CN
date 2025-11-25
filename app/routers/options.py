from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status, UploadFile, File, Body
from pydantic import BaseModel
import hashlib
import logging
import uuid
import asyncio
from fastapi.responses import JSONResponse

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.option_data_service import OptionDataService

router = APIRouter(prefix="/api/options", tags=["options"])
logger = logging.getLogger("webapi")

# 简单的内存缓存
_options_list_cache = {}
_cache_ttl_seconds = 300  # 5分钟缓存


@router.get("/overview")
async def get_options_overview(current_user: dict = Depends(get_current_user)):
    """获取期权概览数据"""
    try:
        db = get_mongo_db()
        
        # 统计数据
        stats = {
            "total_contracts": 0,
            "categories": [],
            "recent_performance": {},
            "message": "期权概览功能正在开发中"
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取期权概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections")
async def list_options_collections(current_user: dict = Depends(get_current_user)):
    """获取期权数据集合列表"""
    try:
        # 定义期权数据集合
        collections = [
            {
                "name": "options_basic_info",
                "display_name": "期权基础信息",
                "description": "期权合约的基础信息，包括代码、名称、标的资产、行权价等",
                "route": "/options/collections/options_basic_info",
                "fields": ["code", "name", "underlying", "strike_price", "option_type", "expiry_date"],
            },
            {
                "name": "options_daily_quotes",
                "display_name": "期权日行情",
                "description": "期权合约的历史日行情数据",
                "route": "/options/collections/options_daily_quotes",
                "fields": ["code", "date", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "options_greeks",
                "display_name": "期权希腊值",
                "description": "期权的希腊字母指标数据",
                "route": "/options/collections/options_greeks",
                "fields": ["code", "date", "delta", "gamma", "theta", "vega", "rho"],
            },
            {
                "name": "option_contract_info_ctp",
                "display_name": "OpenCTP期权合约信息",
                "description": "OpenCTP期权合约信息，包括合约ID、名称、保证金率、手续费率等",
                "route": "/options/collections/option_contract_info_ctp",
                "fields": ["exchange_id", "instrument_id", "instrument_name", "product_class"],
            },
            {
                "name": "option_finance_board",
                "display_name": "金融期权行情数据",
                "description": "上海证券交易所、深圳证券交易所、中国金融期货交易所的金融期权行情数据",
                "route": "/options/collections/option_finance_board",
                "fields": ["date", "code", "current_price", "change_pct", "strike_price", "symbol", "end_month"],
            },
            {
                "name": "option_risk_indicator_sse",
                "display_name": "期权风险指标",
                "description": "上海证券交易所-产品-股票期权-期权风险指标数据",
                "route": "/options/collections/option_risk_indicator_sse",
                "fields": ["trade_date", "contract_id", "contract_symbol", "delta", "gamma", "theta", "vega", "rho"],
            },
            {
                "name": "option_current_day_sse",
                "display_name": "信息披露当日合约",
                "description": "上海证券交易所-产品-股票期权-信息披露-当日合约",
                "route": "/options/collections/option_current_day_sse",
                "fields": ["contract_code", "trade_code", "contract_name", "underlying_name_code", "option_type", "strike_price", "contract_unit", "expire_date"],
            },
            {
                "name": "option_current_day_szse",
                "display_name": "深圳期权当日合约",
                "description": "深圳证券交易所-期权子网-行情数据-当日合约",
                "route": "/options/collections/option_current_day_szse",
                "fields": ["contract_code", "contract_name", "underlying_name_code", "contract_type", "strike_price", "expire_date", "limit_up", "limit_down"],
            },
            {
                "name": "option_daily_stats_sse",
                "display_name": "上交所期权每日统计",
                "description": "上海证券交易所-产品-股票期权-每日统计",
                "route": "/options/collections/option_daily_stats_sse",
                "fields": ["trade_date", "underlying_code", "underlying_name", "contract_quantity", "total_turnover", "total_volume", "put_call_ratio"],
            },
            {
                "name": "option_daily_stats_szse",
                "display_name": "深交所期权每日统计",
                "description": "深圳证券交易所-市场数据-期权数据-日度概况",
                "route": "/options/collections/option_daily_stats_szse",
                "fields": ["trade_date", "underlying_code", "underlying_name", "total_volume", "put_call_ratio", "open_interest_total"],
            },
            {
                "name": "option_cffex_sz50_list_sina",
                "display_name": "中金所上证50期权合约",
                "description": "中金所-上证50指数-所有合约",
                "route": "/options/collections/option_cffex_sz50_list_sina",
                "fields": ["contract_code"],
            },
            {
                "name": "option_cffex_hs300_list_sina",
                "display_name": "中金所沪深300期权合约",
                "description": "中金所-沪深300指数-所有合约",
                "route": "/options/collections/option_cffex_hs300_list_sina",
                "fields": ["contract_code"],
            },
            {
                "name": "option_cffex_zz1000_list_sina",
                "display_name": "中金所中证1000期权合约",
                "description": "中金所-中证1000指数-所有合约",
                "route": "/options/collections/option_cffex_zz1000_list_sina",
                "fields": ["contract_code"],
            },
            {
                "name": "option_cffex_sz50_spot_sina",
                "display_name": "中金所上证50指数实时行情",
                "description": "新浪财经-中金所-上证50指数-指定合约-实时行情",
                "route": "/options/collections/option_cffex_sz50_spot_sina",
                "fields": ["symbol", "strike_price", "call_last_price", "put_last_price", "call_symbol", "put_symbol"],
            },
            {
                "name": "option_cffex_hs300_spot_sina",
                "display_name": "中金所沪深300指数实时行情",
                "description": "新浪财经-中金所-沪深300指数-指定合约-实时行情",
                "route": "/options/collections/option_cffex_hs300_spot_sina",
                "fields": ["symbol", "strike_price", "call_last_price", "put_last_price", "call_symbol", "put_symbol"],
            },
            {
                "name": "option_cffex_zz1000_spot_sina",
                "display_name": "中金所中证1000指数实时行情",
                "description": "新浪财经-中金所-中证1000指数-指定合约-实时行情",
                "route": "/options/collections/option_cffex_zz1000_spot_sina",
                "fields": ["symbol", "strike_price", "call_last_price", "put_last_price", "call_symbol", "put_symbol"],
            },
            {
                "name": "option_cffex_sz50_daily_sina",
                "display_name": "中金所上证50指数日频行情",
                "description": "中金所-上证50指数-指定合约-日频行情",
                "route": "/options/collections/option_cffex_sz50_daily_sina",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume"],
            },
            {
                "name": "option_cffex_hs300_daily_sina",
                "display_name": "中金所沪深300指数日频行情",
                "description": "中金所-沪深300指数-指定合约-日频行情",
                "route": "/options/collections/option_cffex_hs300_daily_sina",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume"],
            },
            {
                "name": "option_cffex_zz1000_daily_sina",
                "display_name": "中金所中证1000指数日频行情",
                "description": "中金所-中证1000指数-指定合约-日频行情",
                "route": "/options/collections/option_cffex_zz1000_daily_sina",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume"],
            },
            {
                "name": "option_sse_list_sina",
                "display_name": "上交所ETF合约到期月份",
                "description": "上交所-50ETF/300ETF-合约到期月份列表",
                "route": "/options/collections/option_sse_list_sina",
                "fields": ["symbol", "month"],
            },
            {
                "name": "option_sse_expire_day_sina",
                "display_name": "上交所ETF剩余到期时间",
                "description": "指定到期月份指定品种的剩余到期时间",
                "route": "/options/collections/option_sse_expire_day_sina",
                "fields": ["trade_date", "symbol", "expire_days"],
            },
            {
                "name": "option_sse_codes_sina",
                "display_name": "新浪期权合约代码",
                "description": "新浪期权看涨看跌合约的代码",
                "route": "/options/collections/option_sse_codes_sina",
                "fields": ["trade_date", "symbol", "contract_code"],
            },
            {
                "name": "option_current_em",
                "display_name": "期权实时数据",
                "description": "期权实时行情数据",
                "route": "/options/collections/option_current_em",
                "fields": ["code", "name", "latest_price", "change_pct", "volume", "open_interest"],
            },
            {
                "name": "option_sse_underlying_spot_price_sina",
                "display_name": "期权标的物实时数据",
                "description": "获取期权标的物的实时数据",
                "route": "/options/collections/option_sse_underlying_spot_price_sina",
                "fields": ["symbol", "field", "value"],
            },
            {
                "name": "option_sse_greeks_sina",
                "display_name": "期权希腊字母",
                "description": "新浪财经期权希腊字母信息表",
                "route": "/options/collections/option_sse_greeks_sina",
                "fields": ["symbol", "delta", "gamma", "theta", "vega", "rho"],
            },
            {
                "name": "option_sse_minute_sina",
                "display_name": "期权分钟行情",
                "description": "期权行情分钟数据（仅当天）",
                "route": "/options/collections/option_sse_minute_sina",
                "fields": ["symbol", "datetime", "price", "volume"],
            },
            {
                "name": "option_sse_daily_sina",
                "display_name": "期权日行情",
                "description": "期权行情日数据",
                "route": "/options/collections/option_sse_daily_sina",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume"],
            },
            {
                "name": "option_finance_minute_sina",
                "display_name": "新浪期权分时行情",
                "description": "新浪财经-金融期权-股票期权分时行情数据",
                "route": "/options/collections/option_finance_minute_sina",
                "fields": ["symbol", "date", "time", "price", "average_price", "volume"],
            },
            {
                "name": "option_minute_em",
                "display_name": "东财期权分时行情",
                "description": "东方财富网-期权市场分时行情",
                "route": "/options/collections/option_minute_em",
                "fields": ["symbol", "datetime", "price", "volume"],
            },
            {
                "name": "option_lhb_em",
                "display_name": "期权龙虎榜",
                "description": "东方财富网-期权龙虎榜单-金融期权",
                "route": "/options/collections/option_lhb_em",
                "fields": ["rank", "code", "name", "latest_price", "change_pct", "volume", "turnover"],
            },
            {
                "name": "option_value_analysis_em",
                "display_name": "期权价值分析",
                "description": "东方财富网-期权价值分析",
                "route": "/options/collections/option_value_analysis_em",
                "fields": ["code", "name", "latest_price", "intrinsic_value", "time_value"],
            },
            {
                "name": "option_risk_analysis_em",
                "display_name": "期权风险分析",
                "description": "东方财富网-期权风险分析",
                "route": "/options/collections/option_risk_analysis_em",
                "fields": ["code", "name", "leverage_ratio", "delta", "gamma", "theta", "vega"],
            },
            {
                "name": "option_premium_analysis_em",
                "display_name": "期权折溢价",
                "description": "东方财富网-期权折溢价分析",
                "route": "/options/collections/option_premium_analysis_em",
                "fields": ["code", "name", "premium_rate"],
            },
            {
                "name": "option_commodity_contract_sina",
                "display_name": "商品期权在交易合约",
                "description": "新浪财经-商品期权-当前在交易的合约",
                "route": "/options/collections/option_commodity_contract_sina",
                "fields": ["symbol", "contract"],
            },
            {
                "name": "option_commodity_contract_table_sina",
                "display_name": "商品期权T型报价表",
                "description": "新浪财经-商品期权-T型报价表",
                "route": "/options/collections/option_commodity_contract_table_sina",
                "fields": ["symbol", "contract", "call_code", "call_price", "strike_price", "put_code", "put_price"],
            },
            {
                "name": "option_commodity_hist_sina",
                "display_name": "商品期权历史行情",
                "description": "新浪财经-商品期权-历史行情数据(日频)",
                "route": "/options/collections/option_commodity_hist_sina",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "option_comm_info",
                "display_name": "商品期权手续费",
                "description": "九期网-商品期权手续费数据",
                "route": "/options/collections/option_comm_info",
                "fields": ["exchange", "symbol", "fee_type", "fee_rate"],
            },
            {
                "name": "option_margin",
                "display_name": "期权保证金",
                "description": "唯爱期货-期权保证金",
                "route": "/options/collections/option_margin",
                "fields": ["exchange", "symbol", "margin_rate"],
            },
            {
                "name": "option_hist_shfe",
                "display_name": "上期所商品期权",
                "description": "上海期货交易所-商品期权数据",
                "route": "/options/collections/option_hist_shfe",
                "fields": ["trade_date", "symbol", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "option_hist_dce",
                "display_name": "大商所商品期权",
                "description": "大连商品交易所-商品期权数据",
                "route": "/options/collections/option_hist_dce",
                "fields": ["trade_date", "symbol", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "option_hist_czce",
                "display_name": "郑商所商品期权",
                "description": "郑州商品交易所-商品期权数据",
                "route": "/options/collections/option_hist_czce",
                "fields": ["trade_date", "symbol", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "option_hist_gfex",
                "display_name": "广期所商品期权",
                "description": "广州期货交易所-商品期权数据",
                "route": "/options/collections/option_hist_gfex",
                "fields": ["trade_date", "symbol", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "option_vol_gfex",
                "display_name": "广期所隐含波动率",
                "description": "广州期货交易所-隐含波动率参考值",
                "route": "/options/collections/option_vol_gfex",
                "fields": ["trade_date", "symbol", "implied_volatility"],
            },
            {
                "name": "option_czce_hist",
                "display_name": "郑商所期权历史行情",
                "description": "郑州商品交易所-期权历史行情数据",
                "route": "/options/collections/option_czce_hist",
                "fields": ["trade_date", "symbol", "open", "high", "low", "close", "volume", "open_interest"],
            },
        ]
        
        return {
            "success": True,
            "data": collections
        }
    except Exception as e:
        logger.error(f"获取期权集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}")
async def get_options_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量，默认50"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: dict = Depends(get_current_user),
):
    """获取指定期权集合的数据（分页）"""
    db = get_mongo_db()
    
    # 集合映射
    collection_map = {
        "options_basic_info": db.get_collection("options_basic_info"),
        "options_daily_quotes": db.get_collection("options_daily_quotes"),
        "options_greeks": db.get_collection("options_greeks"),
        "option_contract_info_ctp": db.get_collection("option_contract_info_ctp"),
        "option_finance_board": db.get_collection("option_finance_board"),
        "option_risk_indicator_sse": db.get_collection("option_risk_indicator_sse"),
        "option_current_day_sse": db.get_collection("option_current_day_sse"),
        "option_current_day_szse": db.get_collection("option_current_day_szse"),
        "option_daily_stats_sse": db.get_collection("option_daily_stats_sse"),
        "option_daily_stats_szse": db.get_collection("option_daily_stats_szse"),
        "option_cffex_sz50_list_sina": db.get_collection("option_cffex_sz50_list_sina"),
        "option_cffex_hs300_list_sina": db.get_collection("option_cffex_hs300_list_sina"),
        "option_cffex_zz1000_list_sina": db.get_collection("option_cffex_zz1000_list_sina"),
        "option_cffex_sz50_spot_sina": db.get_collection("option_cffex_sz50_spot_sina"),
        "option_cffex_hs300_spot_sina": db.get_collection("option_cffex_hs300_spot_sina"),
        "option_cffex_zz1000_spot_sina": db.get_collection("option_cffex_zz1000_spot_sina"),
        "option_cffex_sz50_daily_sina": db.get_collection("option_cffex_sz50_daily_sina"),
        "option_cffex_hs300_daily_sina": db.get_collection("option_cffex_hs300_daily_sina"),
        "option_cffex_zz1000_daily_sina": db.get_collection("option_cffex_zz1000_daily_sina"),
        "option_sse_list_sina": db.get_collection("option_sse_list_sina"),
        "option_sse_expire_day_sina": db.get_collection("option_sse_expire_day_sina"),
        "option_sse_codes_sina": db.get_collection("option_sse_codes_sina"),
        "option_current_em": db.get_collection("option_current_em"),
        "option_sse_underlying_spot_price_sina": db.get_collection("option_sse_underlying_spot_price_sina"),
        "option_sse_greeks_sina": db.get_collection("option_sse_greeks_sina"),
        "option_sse_minute_sina": db.get_collection("option_sse_minute_sina"),
        "option_sse_daily_sina": db.get_collection("option_sse_daily_sina"),
        "option_finance_minute_sina": db.get_collection("option_finance_minute_sina"),
        "option_minute_em": db.get_collection("option_minute_em"),
        "option_lhb_em": db.get_collection("option_lhb_em"),
        "option_value_analysis_em": db.get_collection("option_value_analysis_em"),
        "option_risk_analysis_em": db.get_collection("option_risk_analysis_em"),
        "option_premium_analysis_em": db.get_collection("option_premium_analysis_em"),
        "option_commodity_contract_sina": db.get_collection("option_commodity_contract_sina"),
        "option_commodity_contract_table_sina": db.get_collection("option_commodity_contract_table_sina"),
        "option_commodity_hist_sina": db.get_collection("option_commodity_hist_sina"),
        "option_comm_info": db.get_collection("option_comm_info"),
        "option_margin": db.get_collection("option_margin"),
        "option_hist_shfe": db.get_collection("option_hist_shfe"),
        "option_hist_dce": db.get_collection("option_hist_dce"),
        "option_hist_czce": db.get_collection("option_hist_czce"),
        "option_hist_gfex": db.get_collection("option_hist_gfex"),
        "option_vol_gfex": db.get_collection("option_vol_gfex"),
        "option_czce_hist": db.get_collection("option_czce_hist"),
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
                if filter_field_stripped in ["code", "name", "underlying"]:
                    query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                else:
                    query[filter_field_stripped] = filter_value_stripped
        
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
                    fields_info.append({
                        "name": key,
                        "type": field_type,
                        "example": str(value)[:50] if value is not None else None,
                    })
        
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
        logger.error(f"获取期权集合 {collection_name} 数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/data")
async def get_options_collection_data_alias(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量，默认50"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: dict = Depends(get_current_user),
):
    """与 /collections/{collection_name} 相同的数据获取接口，兼容 tests 中的 /data 路径"""
    return await get_options_collection_data(
        collection_name=collection_name,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_dir=sort_dir,
        filter_field=filter_field,
        filter_value=filter_value,
        current_user=current_user,
    )


@router.post("/collections/{collection_name}/refresh")
async def refresh_options_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    """刷新期权集合数据"""
    try:
        db = get_mongo_db()
        service = OptionDataService(db)
        
        if collection_name == "option_contract_info_ctp":
            # 使用后台任务执行刷新
            background_tasks.add_task(service.fetch_and_save_option_contract_info_ctp)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_finance_board":
            background_tasks.add_task(service.fetch_and_save_option_finance_board)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_risk_indicator_sse":
            background_tasks.add_task(service.fetch_and_save_option_risk_indicator_sse)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_current_day_sse":
            background_tasks.add_task(service.fetch_and_save_option_current_day_sse)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_current_day_szse":
            background_tasks.add_task(service.fetch_and_save_option_current_day_szse)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_daily_stats_sse":
            background_tasks.add_task(service.fetch_and_save_option_daily_stats_sse)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_daily_stats_szse":
            background_tasks.add_task(service.fetch_and_save_option_daily_stats_szse)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}

        if collection_name == "option_cffex_sz50_list_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_sz50_list_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_hs300_list_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_hs300_list_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_zz1000_list_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_zz1000_list_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_sz50_spot_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_sz50_spot_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_hs300_spot_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_hs300_spot_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_zz1000_spot_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_zz1000_spot_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_sz50_daily_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_sz50_daily_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_hs300_daily_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_hs300_daily_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_cffex_zz1000_daily_sina":
            background_tasks.add_task(service.fetch_and_save_option_cffex_zz1000_daily_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_list_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_list_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_expire_day_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_expire_day_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_codes_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_codes_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_current_em":
            background_tasks.add_task(service.fetch_and_save_option_current_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_underlying_spot_price_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_underlying_spot_price_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_greeks_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_greeks_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_minute_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_minute_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_sse_daily_sina":
            background_tasks.add_task(service.fetch_and_save_option_sse_daily_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_finance_minute_sina":
            background_tasks.add_task(service.fetch_and_save_option_finance_minute_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_minute_em":
            background_tasks.add_task(service.fetch_and_save_option_minute_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_lhb_em":
            background_tasks.add_task(service.fetch_and_save_option_lhb_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_value_analysis_em":
            background_tasks.add_task(service.fetch_and_save_option_value_analysis_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_risk_analysis_em":
            background_tasks.add_task(service.fetch_and_save_option_risk_analysis_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_premium_analysis_em":
            background_tasks.add_task(service.fetch_and_save_option_premium_analysis_em)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_commodity_contract_sina":
            background_tasks.add_task(service.fetch_and_save_option_commodity_contract_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_commodity_contract_table_sina":
            background_tasks.add_task(service.fetch_and_save_option_commodity_contract_table_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_commodity_hist_sina":
            background_tasks.add_task(service.fetch_and_save_option_commodity_hist_sina)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_comm_info":
            background_tasks.add_task(service.fetch_and_save_option_comm_info)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_margin":
            background_tasks.add_task(service.fetch_and_save_option_margin)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_hist_shfe":
            background_tasks.add_task(service.fetch_and_save_option_hist_shfe)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_hist_dce":
            background_tasks.add_task(service.fetch_and_save_option_hist_dce)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_hist_czce":
            background_tasks.add_task(service.fetch_and_save_option_hist_czce)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_hist_gfex":
            background_tasks.add_task(service.fetch_and_save_option_hist_gfex)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_vol_gfex":
            background_tasks.add_task(service.fetch_and_save_option_vol_gfex)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        if collection_name == "option_czce_hist":
            background_tasks.add_task(service.fetch_and_save_option_czce_hist)
            return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
        
        return {"success": False, "error": f"不支持刷新集合 {collection_name}"}
    except Exception as e:
        logger.error(f"刷新期权集合 {collection_name} 失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/upload")
async def upload_option_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传期权数据文件"""
    try:
        if not file.filename.endswith((".csv", ".xls", ".xlsx")):
            return {"success": False, "error": "只支持CSV或Excel文件"}

        db = get_mongo_db()
        service = OptionDataService(db)

        # 读取文件内容
        content = await file.read()
        filename = file.filename

        result = await service.import_data_from_file(collection_name, content, filename)

        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        logger.error(f"上传期权文件失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/sync")
async def sync_option_data(
    collection_name: str,
    sync_config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """远程同步期权数据"""
    try:
        db = get_mongo_db()
        service = OptionDataService(db)

        result = await service.sync_data_from_remote(collection_name, sync_config)

        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        logger.error(f"远程同步期权数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/clear")
async def clear_options_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空期权集合数据"""
    try:
        db = get_mongo_db()
        service = OptionDataService(db)
        
        if collection_name == "option_contract_info_ctp":
            count = await service.clear_option_contract_info_ctp()
            return {"success": True, "message": f"已清空 {count} 条数据"}
            
        if collection_name == "option_finance_board":
            count = await service.clear_option_finance_board()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_risk_indicator_sse":
            count = await service.clear_option_risk_indicator_sse()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_current_day_sse":
            count = await service.clear_option_current_day_sse()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_current_day_szse":
            count = await service.clear_option_current_day_szse()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_daily_stats_sse":
            count = await service.clear_option_daily_stats_sse()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_daily_stats_szse":
            count = await service.clear_option_daily_stats_szse()
            return {"success": True, "message": f"已清空 {count} 条数据"}

        if collection_name == "option_cffex_sz50_list_sina":
            count = await service.clear_option_cffex_sz50_list_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_hs300_list_sina":
            count = await service.clear_option_cffex_hs300_list_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_zz1000_list_sina":
            count = await service.clear_option_cffex_zz1000_list_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_sz50_spot_sina":
            count = await service.clear_option_cffex_sz50_spot_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_hs300_spot_sina":
            count = await service.clear_option_cffex_hs300_spot_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_zz1000_spot_sina":
            count = await service.clear_option_cffex_zz1000_spot_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_sz50_daily_sina":
            count = await service.clear_option_cffex_sz50_daily_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_hs300_daily_sina":
            count = await service.clear_option_cffex_hs300_daily_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_cffex_zz1000_daily_sina":
            count = await service.clear_option_cffex_zz1000_daily_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_list_sina":
            count = await service.clear_option_sse_list_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_expire_day_sina":
            count = await service.clear_option_sse_expire_day_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_codes_sina":
            count = await service.clear_option_sse_codes_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_current_em":
            count = await service.clear_option_current_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_underlying_spot_price_sina":
            count = await service.clear_option_sse_underlying_spot_price_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_greeks_sina":
            count = await service.clear_option_sse_greeks_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_minute_sina":
            count = await service.clear_option_sse_minute_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_sse_daily_sina":
            count = await service.clear_option_sse_daily_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_finance_minute_sina":
            count = await service.clear_option_finance_minute_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_minute_em":
            count = await service.clear_option_minute_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_lhb_em":
            count = await service.clear_option_lhb_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_value_analysis_em":
            count = await service.clear_option_value_analysis_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_risk_analysis_em":
            count = await service.clear_option_risk_analysis_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_premium_analysis_em":
            count = await service.clear_option_premium_analysis_em()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_commodity_contract_sina":
            count = await service.clear_option_commodity_contract_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_commodity_contract_table_sina":
            count = await service.clear_option_commodity_contract_table_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_commodity_hist_sina":
            count = await service.clear_option_commodity_hist_sina()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_comm_info":
            count = await service.clear_option_comm_info()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_margin":
            count = await service.clear_option_margin()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_hist_shfe":
            count = await service.clear_option_hist_shfe()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_hist_dce":
            count = await service.clear_option_hist_dce()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_hist_czce":
            count = await service.clear_option_hist_czce()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_hist_gfex":
            count = await service.clear_option_hist_gfex()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_vol_gfex":
            count = await service.clear_option_vol_gfex()
            return {"success": True, "message": f"已清空 {count} 条数据"}
        
        if collection_name == "option_czce_hist":
            count = await service.clear_option_czce_hist()
            return {"success": True, "message": f"已清空 {count} 条数据"}
            
        return {"success": False, "error": f"不支持清空集合 {collection_name}"}
    except Exception as e:
        logger.error(f"清空期权集合 {collection_name} 失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_options_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取期权集合的统计信息"""
    db = get_mongo_db()
    
    collection_map = {
        "options_basic_info": db.get_collection("options_basic_info"),
        "options_daily_quotes": db.get_collection("options_daily_quotes"),
        "options_greeks": db.get_collection("options_greeks"),
        "option_contract_info_ctp": db.get_collection("option_contract_info_ctp"),
        "option_finance_board": db.get_collection("option_finance_board"),
        "option_risk_indicator_sse": db.get_collection("option_risk_indicator_sse"),
        "option_current_day_sse": db.get_collection("option_current_day_sse"),
        "option_current_day_szse": db.get_collection("option_current_day_szse"),
        "option_daily_stats_sse": db.get_collection("option_daily_stats_sse"),
        "option_daily_stats_szse": db.get_collection("option_daily_stats_szse"),
        "option_cffex_sz50_list_sina": db.get_collection("option_cffex_sz50_list_sina"),
        "option_cffex_hs300_list_sina": db.get_collection("option_cffex_hs300_list_sina"),
        "option_cffex_zz1000_list_sina": db.get_collection("option_cffex_zz1000_list_sina"),
        "option_cffex_sz50_spot_sina": db.get_collection("option_cffex_sz50_spot_sina"),
        "option_cffex_hs300_spot_sina": db.get_collection("option_cffex_hs300_spot_sina"),
        "option_cffex_zz1000_spot_sina": db.get_collection("option_cffex_zz1000_spot_sina"),
        "option_cffex_sz50_daily_sina": db.get_collection("option_cffex_sz50_daily_sina"),
        "option_cffex_hs300_daily_sina": db.get_collection("option_cffex_hs300_daily_sina"),
        "option_cffex_zz1000_daily_sina": db.get_collection("option_cffex_zz1000_daily_sina"),
        "option_sse_list_sina": db.get_collection("option_sse_list_sina"),
        "option_sse_expire_day_sina": db.get_collection("option_sse_expire_day_sina"),
        "option_sse_codes_sina": db.get_collection("option_sse_codes_sina"),
        "option_current_em": db.get_collection("option_current_em"),
        "option_sse_underlying_spot_price_sina": db.get_collection("option_sse_underlying_spot_price_sina"),
        "option_sse_greeks_sina": db.get_collection("option_sse_greeks_sina"),
        "option_sse_minute_sina": db.get_collection("option_sse_minute_sina"),
        "option_sse_daily_sina": db.get_collection("option_sse_daily_sina"),
        "option_finance_minute_sina": db.get_collection("option_finance_minute_sina"),
        "option_minute_em": db.get_collection("option_minute_em"),
        "option_lhb_em": db.get_collection("option_lhb_em"),
        "option_value_analysis_em": db.get_collection("option_value_analysis_em"),
        "option_risk_analysis_em": db.get_collection("option_risk_analysis_em"),
        "option_premium_analysis_em": db.get_collection("option_premium_analysis_em"),
        "option_commodity_contract_sina": db.get_collection("option_commodity_contract_sina"),
        "option_commodity_contract_table_sina": db.get_collection("option_commodity_contract_table_sina"),
        "option_commodity_hist_sina": db.get_collection("option_commodity_hist_sina"),
        "option_comm_info": db.get_collection("option_comm_info"),
        "option_margin": db.get_collection("option_margin"),
        "option_hist_shfe": db.get_collection("option_hist_shfe"),
        "option_hist_dce": db.get_collection("option_hist_dce"),
        "option_hist_czce": db.get_collection("option_hist_czce"),
        "option_hist_gfex": db.get_collection("option_hist_gfex"),
        "option_vol_gfex": db.get_collection("option_vol_gfex"),
        "option_czce_hist": db.get_collection("option_czce_hist"),
    }
    
    collection = collection_map.get(collection_name)
    if collection is None:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    
    try:
        total_count = await collection.count_documents({})
        
        stats = {
            "total_count": total_count,
            "collection_name": collection_name,
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取期权集合统计失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/search")
async def search_options(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: dict = Depends(get_current_user),
):
    """搜索期权合约"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("options_basic_info")
        
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
        logger.error(f"搜索期权失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/analysis/{option_code}")
async def get_option_analysis(
    option_code: str,
    current_user: dict = Depends(get_current_user),
):
    """获取期权分析数据"""
    try:
        db = get_mongo_db()
        
        # 获取期权基础信息
        basic_info = await db.get_collection("options_basic_info").find_one({"code": option_code})
        
        if not basic_info:
            return {"success": False, "error": f"未找到期权合约 {option_code}"}
        
        if "_id" in basic_info:
            basic_info["_id"] = str(basic_info["_id"])
        
        # 获取行情数据
        quotes_cursor = db.get_collection("options_daily_quotes").find(
            {"code": option_code}
        ).sort("date", -1).limit(100)
        
        quotes = []
        async for doc in quotes_cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            quotes.append(doc)
        
        # 获取希腊值数据
        greeks_cursor = db.get_collection("options_greeks").find(
            {"code": option_code}
        ).sort("date", -1).limit(100)
        
        greeks = []
        async for doc in greeks_cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            greeks.append(doc)
        
        return {
            "success": True,
            "data": {
                "basic_info": basic_info,
                "quotes": quotes,
                "greeks": greeks,
                "message": "期权分析功能正在开发中"
            }
        }
    except Exception as e:
        logger.error(f"获取期权分析失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
