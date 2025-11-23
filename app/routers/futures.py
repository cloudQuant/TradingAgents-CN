from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
import hashlib
import logging
import uuid
import asyncio
from fastapi.responses import JSONResponse

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

# 导入update任务函数
try:
    from app.services.futures_update_tasks import (
        update_futures_fees_info_task,
        update_futures_comm_info_task,
        update_futures_rule_task,
        update_futures_inventory_99_task,
        update_futures_inventory_em_task,
        update_futures_dce_position_rank_task,
        update_futures_gfex_position_rank_task,
        update_futures_warehouse_receipt_czce_task,
        update_futures_warehouse_receipt_dce_task,
        update_futures_shfe_warehouse_receipt_task,
        update_futures_gfex_warehouse_receipt_task,
        update_futures_to_spot_dce_task,
        update_futures_to_spot_czce_task,
        update_futures_to_spot_shfe_task,
        update_futures_spot_sys_task,
        update_futures_contract_info_shfe_task,
        update_futures_contract_info_ine_task,
        update_futures_contract_info_dce_task,
        update_futures_contract_info_czce_task,
        update_futures_contract_info_gfex_task,
        update_futures_contract_info_cffex_task,
        update_futures_zh_spot_task,
        update_futures_zh_realtime_task,
        update_futures_zh_minute_sina_task,
        update_futures_hist_em_task,
        update_futures_zh_daily_sina_task,
        update_get_futures_daily_task,
        update_futures_hq_subscribe_exchange_symbol_task,
        update_futures_foreign_commodity_realtime_task,
        update_futures_global_spot_em_task,
        update_futures_global_hist_em_task,
        update_futures_foreign_hist_task,
        update_futures_foreign_detail_task,
        update_futures_settlement_price_sgx_task,
        update_futures_main_sina_task,
        update_futures_contract_detail_task,
        update_futures_contract_detail_em_task,
        update_futures_index_ccidx_task,
        update_futures_spot_stock_task,
        update_futures_comex_inventory_task,
        update_futures_hog_core_task,
        update_futures_hog_cost_task,
        update_futures_hog_supply_task,
        update_index_hog_spot_price_task,
        update_futures_news_shmet_task,
    )
except ImportError as e:
    logger = logging.getLogger("webapi")
    logger.warning(f"futures_update_tasks import error: {e}")

router = APIRouter(prefix="/api/futures", tags=["futures"])
logger = logging.getLogger("webapi")

# 简单的内存缓存
_futures_list_cache = {}
_cache_ttl_seconds = 300  # 5分钟缓存


@router.get("/overview")
async def get_futures_overview(current_user: dict = Depends(get_current_user)):
    """获取期货概览数据"""
    try:
        db = get_mongo_db()
        
        # 统计数据
        stats = {
            "total_contracts": 0,
            "categories": [],
            "recent_performance": {},
            "message": "期货概览功能正在开发中"
        }
        
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"获取期货概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections")
async def list_futures_collections(current_user: dict = Depends(get_current_user)):
    """获取期货数据集合列表"""
    try:
        # 定义期货数据集合
        collections = [
            {
                "name": "futures_basic_info",
                "display_name": "期货基础信息",
                "description": "期货合约的基础信息，包括代码、名称、交易所、合约规格等",
                "route": "/futures/collections/futures_basic_info",
                "fields": ["code", "name", "exchange", "underlying_asset", "contract_size", "delivery_month"],
            },
            {
                "name": "futures_daily_quotes",
                "display_name": "期货日行情",
                "description": "期货合约的历史日行情数据",
                "route": "/futures/collections/futures_daily_quotes",
                "fields": ["code", "date", "open", "high", "low", "close", "volume", "open_interest"],
            },
            {
                "name": "futures_dominant_contracts",
                "display_name": "主力合约",
                "description": "期货品种的主力合约数据",
                "route": "/futures/collections/futures_dominant_contracts",
                "fields": ["symbol", "dominant_contract", "date", "volume", "open_interest"],
            },
            {
                "name": "futures_fees_info",
                "display_name": "期货交易费用参照表",
                "description": "openctp 期货交易费用参照表",
                "route": "/futures/collections/futures_fees_info",
                "fields": ["交易所", "合约代码", "合约名称", "品种代码", "品种名称", "合约乘数", "最小跳动", "最新价"],
            },
            {
                "name": "futures_comm_info",
                "display_name": "期货手续费与保证金",
                "description": "九期网-期货手续费数据",
                "route": "/futures/collections/futures_comm_info",
                "fields": ["交易所名称", "合约名称", "合约代码", "现价", "涨停板", "跌停板", "保证金-买开", "保证金-卖开"],
            },
            {
                "name": "futures_rule",
                "display_name": "期货规则-交易日历表",
                "description": "国泰君安期货-交易日历数据表",
                "route": "/futures/collections/futures_rule",
                "fields": ["交易所", "品种", "代码", "交易保证金比例", "涨跌停板幅度", "合约乘数", "最小变动价位"],
            },
            {
                "name": "futures_inventory_99",
                "display_name": "库存数据-99期货网",
                "description": "99 期货网-大宗商品库存数据",
                "route": "/futures/collections/futures_inventory_99",
                "fields": ["日期", "收盘价", "库存", "symbol"],
            },
            {
                "name": "futures_inventory_em",
                "display_name": "库存数据-东方财富",
                "description": "东方财富网-期货数据-库存数据",
                "route": "/futures/collections/futures_inventory_em",
                "fields": ["日期", "库存", "增减", "symbol"],
            },
            {
                "name": "futures_dce_position_rank",
                "display_name": "大连商品交易所",
                "description": "大连商品交易所指定交易日的具体合约的持仓排名",
                "route": "/futures/collections/futures_dce_position_rank",
                "fields": ["date", "symbol", "rank", "member_name", "vol", "vol_chg"],
            },
            {
                "name": "futures_gfex_position_rank",
                "display_name": "广州期货交易所",
                "description": "广州期货交易所-日成交持仓排名",
                "route": "/futures/collections/futures_gfex_position_rank",
                "fields": ["date", "symbol", "rank", "member_name", "vol", "vol_chg"],
            },
            {
                "name": "futures_warehouse_receipt_czce",
                "display_name": "仓单日报-郑州商品交易所",
                "description": "郑州商品交易所-交易数据-仓单日报",
                "route": "/futures/collections/futures_warehouse_receipt_czce",
                "fields": ["date", "symbol", "warehouse", "receipt"],
            },
            {
                "name": "futures_warehouse_receipt_dce",
                "display_name": "仓单日报-大连商品交易所",
                "description": "大连商品交易所-行情数据-统计数据-日统计-仓单日报",
                "route": "/futures/collections/futures_warehouse_receipt_dce",
                "fields": ["date", "symbol", "warehouse", "receipt"],
            },
            {
                "name": "futures_shfe_warehouse_receipt",
                "display_name": "仓单日报-上海期货交易所",
                "description": "上海期货交易所-仓单日报",
                "route": "/futures/collections/futures_shfe_warehouse_receipt",
                "fields": ["date", "symbol", "warehouse", "receipt"],
            },
            {
                "name": "futures_gfex_warehouse_receipt",
                "display_name": "仓单日报-广州期货交易所",
                "description": "广州期货交易所-行情数据-仓单日报",
                "route": "/futures/collections/futures_gfex_warehouse_receipt",
                "fields": ["date", "symbol", "warehouse", "receipt"],
            },
            {
                "name": "futures_to_spot_dce",
                "display_name": "期转现-大商所",
                "description": "大连商品交易所-期转现统计数据",
                "route": "/futures/collections/futures_to_spot_dce",
                "fields": ["date", "合约代码", "期转现发生日期", "期转现数量"],
            },
            {
                "name": "futures_to_spot_czce",
                "display_name": "期转现-郑商所",
                "description": "郑州商品交易所-期转现统计数据",
                "route": "/futures/collections/futures_to_spot_czce",
                "fields": ["date", "合约代码", "合约数量"],
            },
            {
                "name": "futures_to_spot_shfe",
                "display_name": "期转现-上期所",
                "description": "上海期货交易所-期转现数据",
                "route": "/futures/collections/futures_to_spot_shfe",
                "fields": ["date", "日期", "合约", "交割量", "期转现量"],
            },
            {
                "name": "futures_delivery_dce",
                "display_name": "交割统计-大商所",
                "description": "大连商品交易所-交割统计",
                "route": "/futures/collections/futures_delivery_dce",
                "fields": ["date", "品种", "合约", "交割日期", "交割量", "交割金额"],
            },
            {
                "name": "futures_delivery_czce",
                "display_name": "交割统计-郑商所",
                "description": "郑州商品交易所-交割统计",
                "route": "/futures/collections/futures_delivery_czce",
                "fields": ["date", "品种", "交割数量", "交割额"],
            },
            {
                "name": "futures_delivery_shfe",
                "display_name": "交割统计-上期所",
                "description": "上海期货交易所-交割统计",
                "route": "/futures/collections/futures_delivery_shfe",
                "fields": ["date", "品种", "交割量-本月", "交割量-比重", "交割量-本年累计", "交割量-累计同比"],
            },
            {
                "name": "futures_delivery_match_dce",
                "display_name": "交割配对-大商所",
                "description": "大连商品交易所-交割配对",
                "route": "/futures/collections/futures_delivery_match_dce",
                "fields": ["symbol", "合约号", "配对日期", "买会员号", "配对手数", "卖会员号"],
            },
            {
                "name": "futures_delivery_match_czce",
                "display_name": "交割配对-郑商所",
                "description": "郑州商品交易所-交割配对",
                "route": "/futures/collections/futures_delivery_match_czce",
                "fields": ["date", "卖方会员", "卖方会员-会员简称", "买方会员", "买方会员-会员简称", "交割量"],
            },
            {
                "name": "futures_stock_shfe_js",
                "display_name": "上海期货交易所库存周报",
                "description": "金十财经-上海期货交易所指定交割仓库库存周报",
                "route": "/futures/collections/futures_stock_shfe_js",
                "fields": ["date", "商品", "增减", "增减幅度"],
            },
            {
                "name": "futures_hold_pos_sina",
                "display_name": "成交持仓",
                "description": "新浪财经-期货-成交持仓",
                "route": "/futures/collections/futures_hold_pos_sina",
                "fields": ["symbol", "contract", "date", "名次", "会员简称", "成交量"],
            },
            # 022-028 现期图与合约信息
            {
                "name": "futures_spot_sys",
                "display_name": "现期图",
                "description": "生意社-商品与期货-现期图",
                "route": "/futures/collections/futures_spot_sys",
                "fields": ["日期", "主力基差", "symbol", "indicator"],
            },
            {
                "name": "futures_contract_info_shfe",
                "display_name": "上海期货交易所",
                "description": "上海期货交易所-交易参数汇总查询",
                "route": "/futures/collections/futures_contract_info_shfe",
                "fields": ["合约代码", "上市日", "到期日", "开始交割日", "最后交割日", "挂牌基准价"],
            },
            {
                "name": "futures_contract_info_ine",
                "display_name": "上海国际能源交易中心",
                "description": "上海国际能源交易中心-交易参数汇总",
                "route": "/futures/collections/futures_contract_info_ine",
                "fields": ["合约代码", "上市日", "到期日", "开始交割日", "最后交割日", "挂牌基准价"],
            },
            {
                "name": "futures_contract_info_dce",
                "display_name": "大连商品交易所",
                "description": "大连商品交易所-合约信息",
                "route": "/futures/collections/futures_contract_info_dce",
                "fields": ["品种", "合约代码", "交易单位", "最小变动价位", "开始交易日", "最后交易日"],
            },
            {
                "name": "futures_contract_info_czce",
                "display_name": "郑州商品交易所",
                "description": "郑州商品交易所-参考数据",
                "route": "/futures/collections/futures_contract_info_czce",
                "fields": ["产品名称", "合约代码", "产品代码", "交易单位", "最小变动价位"],
            },
            {
                "name": "futures_contract_info_gfex",
                "display_name": "广州期货交易所",
                "description": "广州期货交易所-合约信息",
                "route": "/futures/collections/futures_contract_info_gfex",
                "fields": ["品种", "合约代码", "交易单位", "最小变动单位", "开始交易日", "最后交易日"],
            },
            {
                "name": "futures_contract_info_cffex",
                "display_name": "中国金融期货交易所",
                "description": "中国金融期货交易所-交易参数",
                "route": "/futures/collections/futures_contract_info_cffex",
                "fields": ["合约代码", "合约月份", "挂盘基准价", "上市日", "最后交易日"],
            },
            # 029-034 内盘行情
            {
                "name": "futures_zh_spot",
                "display_name": "内盘-实时行情数据",
                "description": "新浪财经-期货实时行情",
                "route": "/futures/collections/futures_zh_spot",
                "fields": ["symbol", "time", "open", "high", "low", "current_price", "volume"],
            },
            {
                "name": "futures_zh_realtime",
                "display_name": "内盘-实时行情数据(品种)",
                "description": "新浪财经-期货实时行情(按品种)",
                "route": "/futures/collections/futures_zh_realtime",
                "fields": ["symbol", "exchange", "name", "trade", "open", "high", "low", "volume"],
            },
            {
                "name": "futures_zh_minute_sina",
                "display_name": "内盘-分时行情数据",
                "description": "新浪财经-期货分时数据",
                "route": "/futures/collections/futures_zh_minute_sina",
                "fields": ["datetime", "open", "high", "low", "close", "volume", "hold"],
            },
            {
                "name": "futures_hist_em",
                "display_name": "内盘-历史行情数据-东财",
                "description": "东方财富网-期货历史行情",
                "route": "/futures/collections/futures_hist_em",
                "fields": ["时间", "开盘", "最高", "最低", "收盘", "涨跌", "涨跌幅", "成交量"],
            },
            {
                "name": "futures_zh_daily_sina",
                "display_name": "内盘-历史行情数据-新浪",
                "description": "新浪财经-期货日频数据",
                "route": "/futures/collections/futures_zh_daily_sina",
                "fields": ["date", "open", "high", "low", "close", "volume", "hold", "settle"],
            },
            {
                "name": "get_futures_daily",
                "display_name": "内盘-历史行情数据-交易所",
                "description": "各交易所期货历史数据",
                "route": "/futures/collections/get_futures_daily",
                "fields": ["symbol", "date", "open", "high", "low", "close", "volume", "open_interest"],
            },
            # 035-040 外盘期货
            {
                "name": "futures_hq_subscribe_exchange_symbol",
                "display_name": "外盘-品种代码表",
                "description": "新浪财经-外盘期货品种代码表",
                "route": "/futures/collections/futures_hq_subscribe_exchange_symbol",
                "fields": ["symbol", "code"],
            },
            {
                "name": "futures_foreign_commodity_realtime",
                "display_name": "外盘-实时行情数据",
                "description": "新浪财经-外盘商品期货实时数据",
                "route": "/futures/collections/futures_foreign_commodity_realtime",
                "fields": ["名称", "最新价", "人民币报价", "涨跌额", "涨跌幅", "开盘价"],
            },
            {
                "name": "futures_global_spot_em",
                "display_name": "外盘-实时行情数据-东财",
                "description": "东方财富网-国际期货实时行情",
                "route": "/futures/collections/futures_global_spot_em",
                "fields": ["序号", "代码", "名称", "最新价", "涨跌额", "涨跌幅", "今开"],
            },
            {
                "name": "futures_global_hist_em",
                "display_name": "外盘-历史行情数据-东财",
                "description": "东方财富网-国际期货历史行情",
                "route": "/futures/collections/futures_global_hist_em",
                "fields": ["日期", "代码", "名称", "开盘", "最新价", "最高", "最低"],
            },
            {
                "name": "futures_foreign_hist",
                "display_name": "外盘-历史行情数据-新浪",
                "description": "新浪财经-外盘期货历史行情",
                "route": "/futures/collections/futures_foreign_hist",
                "fields": ["date", "open", "high", "low", "close", "volume"],
            },
            {
                "name": "futures_foreign_detail",
                "display_name": "外盘-合约详情",
                "description": "新浪财经-外盘期货合约详情",
                "route": "/futures/collections/futures_foreign_detail",
                "fields": ["交易品种", "最小变动价位", "交易时间", "交易代码"],
            },
            # 041-046 连续合约与指数
            {
                "name": "futures_settlement_price_sgx",
                "display_name": "新加坡交易所期货",
                "description": "新加坡交易所-历史结算价格",
                "route": "/futures/collections/futures_settlement_price_sgx",
                "fields": ["DATE", "COM", "OPEN", "HIGH", "LOW", "CLOSE", "SETTLE"],
            },
            {
                "name": "futures_main_sina",
                "display_name": "期货连续合约",
                "description": "新浪财经-主力连续合约历史数据",
                "route": "/futures/collections/futures_main_sina",
                "fields": ["日期", "开盘价", "最高价", "最低价", "收盘价", "成交量", "持仓量"],
            },
            {
                "name": "futures_contract_detail",
                "display_name": "期货合约详情-新浪",
                "description": "新浪财经-期货合约详情",
                "route": "/futures/collections/futures_contract_detail",
                "fields": ["item", "value"],
            },
            {
                "name": "futures_contract_detail_em",
                "display_name": "期货合约详情-东财",
                "description": "东方财富-期货合约详情",
                "route": "/futures/collections/futures_contract_detail_em",
                "fields": ["item", "value"],
            },
            {
                "name": "futures_index_ccidx",
                "display_name": "中证商品指数",
                "description": "中证商品指数数据",
                "route": "/futures/collections/futures_index_ccidx",
                "fields": ["日期", "指数代码", "收盘点位", "结算点位", "涨跌", "涨跌幅"],
            },
            {
                "name": "futures_spot_stock",
                "display_name": "现货与股票",
                "description": "东方财富网-现货与股票",
                "route": "/futures/collections/futures_spot_stock",
                "fields": ["商品名称", "最新价", "近半年涨跌幅"],
            },
            # 047-052 生猪与资讯
            {
                "name": "futures_comex_inventory",
                "display_name": "COMEX 库存数据",
                "description": "东方财富网-COMEX库存数据",
                "route": "/futures/collections/futures_comex_inventory",
                "fields": ["序号", "日期", "库存量"],
            },
            {
                "name": "futures_hog_core",
                "display_name": "核心数据",
                "description": "玄田数据-核心数据",
                "route": "/futures/collections/futures_hog_core",
                "fields": ["date", "value", "symbol"],
            },
            {
                "name": "futures_hog_cost",
                "display_name": "成本维度",
                "description": "玄田数据-成本维度",
                "route": "/futures/collections/futures_hog_cost",
                "fields": ["date", "value", "symbol"],
            },
            {
                "name": "futures_hog_supply",
                "display_name": "供应维度",
                "description": "玄田数据-供应维度",
                "route": "/futures/collections/futures_hog_supply",
                "fields": ["date", "value", "symbol"],
            },
            {
                "name": "index_hog_spot_price",
                "display_name": "生猪市场价格指数",
                "description": "行情宝-生猪市场价格指数",
                "route": "/futures/collections/index_hog_spot_price",
                "fields": ["日期", "指数", "预售均价", "成交均价", "成交均重"],
            },
            {
                "name": "futures_news_shmet",
                "display_name": "期货资讯",
                "description": "上海金属网-快讯",
                "route": "/futures/collections/futures_news_shmet",
                "fields": ["发布时间", "内容"],
            },
        ]
        
        return {
            "success": True,
            "data": collections
        }
    except Exception as e:
        logger.error(f"获取期货集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}")
async def get_futures_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量，默认50"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: dict = Depends(get_current_user),
):
    """获取指定期货集合的数据（分页）"""
    db = get_mongo_db()
    
    # 集合映射
    collection_map = {
        "futures_basic_info": db.get_collection("futures_basic_info"),
        "futures_daily_quotes": db.get_collection("futures_daily_quotes"),
        "futures_dominant_contracts": db.get_collection("futures_dominant_contracts"),
        "futures_fees_info": db.get_collection("futures_fees_info"),
        "futures_comm_info": db.get_collection("futures_comm_info"),
        "futures_rule": db.get_collection("futures_rule"),
        "futures_inventory_99": db.get_collection("futures_inventory_99"),
        "futures_inventory_em": db.get_collection("futures_inventory_em"),
        "futures_dce_position_rank": db.get_collection("futures_dce_position_rank"),
        "futures_gfex_position_rank": db.get_collection("futures_gfex_position_rank"),
        "futures_warehouse_receipt_czce": db.get_collection("futures_warehouse_receipt_czce"),
        "futures_warehouse_receipt_dce": db.get_collection("futures_warehouse_receipt_dce"),
        "futures_shfe_warehouse_receipt": db.get_collection("futures_shfe_warehouse_receipt"),
        "futures_gfex_warehouse_receipt": db.get_collection("futures_gfex_warehouse_receipt"),
        "futures_to_spot_dce": db.get_collection("futures_to_spot_dce"),
        "futures_to_spot_czce": db.get_collection("futures_to_spot_czce"),
        "futures_to_spot_shfe": db.get_collection("futures_to_spot_shfe"),
        "futures_delivery_dce": db.get_collection("futures_delivery_dce"),
        "futures_delivery_czce": db.get_collection("futures_delivery_czce"),
        "futures_delivery_shfe": db.get_collection("futures_delivery_shfe"),
        "futures_delivery_match_dce": db.get_collection("futures_delivery_match_dce"),
        "futures_delivery_match_czce": db.get_collection("futures_delivery_match_czce"),
        "futures_stock_shfe_js": db.get_collection("futures_stock_shfe_js"),
        "futures_hold_pos_sina": db.get_collection("futures_hold_pos_sina"),
        # 022-052 新增集合
        "futures_spot_sys": db.get_collection("futures_spot_sys"),
        "futures_contract_info_shfe": db.get_collection("futures_contract_info_shfe"),
        "futures_contract_info_ine": db.get_collection("futures_contract_info_ine"),
        "futures_contract_info_dce": db.get_collection("futures_contract_info_dce"),
        "futures_contract_info_czce": db.get_collection("futures_contract_info_czce"),
        "futures_contract_info_gfex": db.get_collection("futures_contract_info_gfex"),
        "futures_contract_info_cffex": db.get_collection("futures_contract_info_cffex"),
        "futures_zh_spot": db.get_collection("futures_zh_spot"),
        "futures_zh_realtime": db.get_collection("futures_zh_realtime"),
        "futures_zh_minute_sina": db.get_collection("futures_zh_minute_sina"),
        "futures_hist_em": db.get_collection("futures_hist_em"),
        "futures_zh_daily_sina": db.get_collection("futures_zh_daily_sina"),
        "get_futures_daily": db.get_collection("get_futures_daily"),
        "futures_hq_subscribe_exchange_symbol": db.get_collection("futures_hq_subscribe_exchange_symbol"),
        "futures_foreign_commodity_realtime": db.get_collection("futures_foreign_commodity_realtime"),
        "futures_global_spot_em": db.get_collection("futures_global_spot_em"),
        "futures_global_hist_em": db.get_collection("futures_global_hist_em"),
        "futures_foreign_hist": db.get_collection("futures_foreign_hist"),
        "futures_foreign_detail": db.get_collection("futures_foreign_detail"),
        "futures_settlement_price_sgx": db.get_collection("futures_settlement_price_sgx"),
        "futures_main_sina": db.get_collection("futures_main_sina"),
        "futures_contract_detail": db.get_collection("futures_contract_detail"),
        "futures_contract_detail_em": db.get_collection("futures_contract_detail_em"),
        "futures_index_ccidx": db.get_collection("futures_index_ccidx"),
        "futures_spot_stock": db.get_collection("futures_spot_stock"),
        "futures_comex_inventory": db.get_collection("futures_comex_inventory"),
        "futures_hog_core": db.get_collection("futures_hog_core"),
        "futures_hog_cost": db.get_collection("futures_hog_cost"),
        "futures_hog_supply": db.get_collection("futures_hog_supply"),
        "index_hog_spot_price": db.get_collection("index_hog_spot_price"),
        "futures_news_shmet": db.get_collection("futures_news_shmet"),
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
                if filter_field_stripped in ["code", "name", "symbol"]:
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
        logger.error(f"获取期货集合 {collection_name} 数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_futures_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取期货集合的统计信息"""
    db = get_mongo_db()
    
    collection_map = {
        "futures_basic_info": db.get_collection("futures_basic_info"),
        "futures_daily_quotes": db.get_collection("futures_daily_quotes"),
        "futures_dominant_contracts": db.get_collection("futures_dominant_contracts"),
        "futures_fees_info": db.get_collection("futures_fees_info"),
        "futures_comm_info": db.get_collection("futures_comm_info"),
        "futures_rule": db.get_collection("futures_rule"),
        "futures_inventory_99": db.get_collection("futures_inventory_99"),
        "futures_inventory_em": db.get_collection("futures_inventory_em"),
        "futures_dce_position_rank": db.get_collection("futures_dce_position_rank"),
        "futures_gfex_position_rank": db.get_collection("futures_gfex_position_rank"),
        "futures_warehouse_receipt_czce": db.get_collection("futures_warehouse_receipt_czce"),
        "futures_warehouse_receipt_dce": db.get_collection("futures_warehouse_receipt_dce"),
        "futures_shfe_warehouse_receipt": db.get_collection("futures_shfe_warehouse_receipt"),
        "futures_gfex_warehouse_receipt": db.get_collection("futures_gfex_warehouse_receipt"),
        "futures_to_spot_dce": db.get_collection("futures_to_spot_dce"),
        "futures_to_spot_czce": db.get_collection("futures_to_spot_czce"),
        "futures_to_spot_shfe": db.get_collection("futures_to_spot_shfe"),
        "futures_delivery_dce": db.get_collection("futures_delivery_dce"),
        "futures_delivery_czce": db.get_collection("futures_delivery_czce"),
        "futures_delivery_shfe": db.get_collection("futures_delivery_shfe"),
        "futures_delivery_match_dce": db.get_collection("futures_delivery_match_dce"),
        "futures_delivery_match_czce": db.get_collection("futures_delivery_match_czce"),
        "futures_stock_shfe_js": db.get_collection("futures_stock_shfe_js"),
        "futures_hold_pos_sina": db.get_collection("futures_hold_pos_sina"),
        # 022-052 新增集合
        "futures_spot_sys": db.get_collection("futures_spot_sys"),
        "futures_contract_info_shfe": db.get_collection("futures_contract_info_shfe"),
        "futures_contract_info_ine": db.get_collection("futures_contract_info_ine"),
        "futures_contract_info_dce": db.get_collection("futures_contract_info_dce"),
        "futures_contract_info_czce": db.get_collection("futures_contract_info_czce"),
        "futures_contract_info_gfex": db.get_collection("futures_contract_info_gfex"),
        "futures_contract_info_cffex": db.get_collection("futures_contract_info_cffex"),
        "futures_zh_spot": db.get_collection("futures_zh_spot"),
        "futures_zh_realtime": db.get_collection("futures_zh_realtime"),
        "futures_zh_minute_sina": db.get_collection("futures_zh_minute_sina"),
        "futures_hist_em": db.get_collection("futures_hist_em"),
        "futures_zh_daily_sina": db.get_collection("futures_zh_daily_sina"),
        "get_futures_daily": db.get_collection("get_futures_daily"),
        "futures_hq_subscribe_exchange_symbol": db.get_collection("futures_hq_subscribe_exchange_symbol"),
        "futures_foreign_commodity_realtime": db.get_collection("futures_foreign_commodity_realtime"),
        "futures_global_spot_em": db.get_collection("futures_global_spot_em"),
        "futures_global_hist_em": db.get_collection("futures_global_hist_em"),
        "futures_foreign_hist": db.get_collection("futures_foreign_hist"),
        "futures_foreign_detail": db.get_collection("futures_foreign_detail"),
        "futures_settlement_price_sgx": db.get_collection("futures_settlement_price_sgx"),
        "futures_main_sina": db.get_collection("futures_main_sina"),
        "futures_contract_detail": db.get_collection("futures_contract_detail"),
        "futures_contract_detail_em": db.get_collection("futures_contract_detail_em"),
        "futures_index_ccidx": db.get_collection("futures_index_ccidx"),
        "futures_spot_stock": db.get_collection("futures_spot_stock"),
        "futures_comex_inventory": db.get_collection("futures_comex_inventory"),
        "futures_hog_core": db.get_collection("futures_hog_core"),
        "futures_hog_cost": db.get_collection("futures_hog_cost"),
        "futures_hog_supply": db.get_collection("futures_hog_supply"),
        "index_hog_spot_price": db.get_collection("index_hog_spot_price"),
        "futures_news_shmet": db.get_collection("futures_news_shmet"),
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
        logger.error(f"获取期货集合统计失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/search")
async def search_futures(
    keyword: str = Query(..., description="搜索关键词"),
    current_user: dict = Depends(get_current_user),
):
    """搜索期货合约"""
    try:
        db = get_mongo_db()
        collection = db.get_collection("futures_basic_info")
        
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
        logger.error(f"搜索期货失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/analysis/{futures_code}")
async def get_futures_analysis(
    futures_code: str,
    current_user: dict = Depends(get_current_user),
):
    """获取期货分析数据"""
    try:
        db = get_mongo_db()
        
        # 获取期货基础信息
        basic_info = await db.get_collection("futures_basic_info").find_one({"code": futures_code})
        
        if not basic_info:
            return {"success": False, "error": f"未找到期货合约 {futures_code}"}
        
        if "_id" in basic_info:
            basic_info["_id"] = str(basic_info["_id"])
        
        # 获取行情数据
        quotes_cursor = db.get_collection("futures_daily_quotes").find(
            {"code": futures_code}
        ).sort("date", -1).limit(100)
        
        quotes = []
        async for doc in quotes_cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            quotes.append(doc)
        
        return {
            "success": True,
            "data": {
                "basic_info": basic_info,
                "quotes": quotes,
                "message": "期货分析功能正在开发中"
            }
        }
    except Exception as e:
        logger.error(f"获取期货分析失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/update")
async def update_futures_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    symbol: Optional[str] = Query(None, description="品种代码/名称，部分集合更新需要"),
    date: Optional[str] = Query(None, description="日期参数，格式根据API要求"),
    market: Optional[str] = Query("CF", description="市场类型: CF-商品期货, FF-金融期货"),
    adjust: Optional[str] = Query("0", description="调整参数: 0-基本数据, 1-详细数据"),
    period: Optional[str] = Query("1", description="周期: 分钟周期1/5/15/30/60或daily/weekly/monthly"),
    start_date: Optional[str] = Query("19900101", description="开始日期，格式YYYYMMDD"),
    end_date: Optional[str] = Query("20500101", description="结束日期，格式YYYYMMDD"),
    current_user: dict = Depends(get_current_user),
):
    """更新期货数据集合"""
    try:
        if collection_name == "futures_fees_info":
            background_tasks.add_task(update_futures_fees_info_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_comm_info":
            query_symbol = symbol if symbol else "所有"
            background_tasks.add_task(update_futures_comm_info_task, query_symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={query_symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_rule":
            # date参数复用symbol字段
            date = symbol if symbol else None
            background_tasks.add_task(update_futures_rule_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date or '自动'})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_inventory_99":
            if not symbol:
                return {"success": False, "error": "更新库存数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_inventory_99_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_inventory_em":
            if not symbol:
                return {"success": False, "error": "更新库存数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_inventory_em_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_dce_position_rank":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_dce_position_rank_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_gfex_position_rank":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_gfex_position_rank_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_warehouse_receipt_czce":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_warehouse_receipt_czce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_warehouse_receipt_dce":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_warehouse_receipt_dce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_shfe_warehouse_receipt":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_shfe_warehouse_receipt_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_gfex_warehouse_receipt":
            # 需要 date 参数
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_gfex_warehouse_receipt_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_to_spot_dce":
            # 需要 date 参数 (年月格式 YYYYMM)
            query_date = date if date else datetime.now().strftime("%Y%m")
            background_tasks.add_task(update_futures_to_spot_dce_task, query_date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={query_date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_to_spot_czce":
            # 需要 date 参数 (YYYYMMDD 格式)
            query_date = date if date else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_to_spot_czce_task, query_date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={query_date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_to_spot_shfe":
            # 需要 date 参数 (年月格式 YYYYMM)
            query_date = date if date else datetime.now().strftime("%Y%m")
            background_tasks.add_task(update_futures_to_spot_shfe_task, query_date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={query_date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_delivery_dce":
            # 需要 date 参数 (年月格式 YYYYMM)
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认当前年月
                date = datetime.now().strftime("%Y%m")
            
            background_tasks.add_task(update_futures_delivery_dce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_delivery_czce":
            # 需要 date 参数 (YYYYMMDD 格式)
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_delivery_czce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_delivery_shfe":
            # 需要 date 参数 (年月格式 YYYYMM)
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认当前年月
                date = datetime.now().strftime("%Y%m")
            
            background_tasks.add_task(update_futures_delivery_shfe_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_delivery_match_dce":
            # 需要 symbol 参数
            if not symbol:
                return {"success": False, "error": "更新交割配对数据需要提供 symbol 参数"}
            
            background_tasks.add_task(update_futures_delivery_match_dce_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_delivery_match_czce":
            # 需要 date 参数 (YYYYMMDD 格式)
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_delivery_match_czce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_stock_shfe_js":
            # 需要 date 参数 (YYYYMMDD 格式)
            date = symbol # 复用 symbol 参数作为 date
            if not date:
                # 如果没传，默认今天
                date = datetime.now().strftime("%Y%m%d")
            
            background_tasks.add_task(update_futures_stock_shfe_js_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hold_pos_sina":
            # 需要 symbol, contract, date 参数，使用冒号分隔
            if not symbol:
                return {"success": False, "error": "更新成交持仓数据需要提供 symbol 参数，格式: symbol:contract:date"}
            
            parts = symbol.split(":")
            if len(parts) != 3:
                return {"success": False, "error": "symbol 参数格式错误，应为: symbol:contract:date"}
            
            pos_symbol, contract, date = parts
            background_tasks.add_task(update_futures_hold_pos_sina_task, pos_symbol, contract, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={pos_symbol}, contract={contract}, date={date})", "task_id": str(uuid.uuid4())}}
        
        # 022-052 新增集合更新逻辑
        elif collection_name == "futures_spot_sys":
            if not symbol:
                return {"success": False, "error": "更新现期图数据需要提供 symbol 参数，格式: symbol:indicator"}
            parts = symbol.split(":")
            if len(parts) != 2:
                return {"success": False, "error": "symbol 参数格式错误，应为: symbol:indicator"}
            sym, indicator = parts
            background_tasks.add_task(update_futures_spot_sys_task, sym, indicator)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={sym}, indicator={indicator})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_shfe":
            date = symbol if symbol else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_contract_info_shfe_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_ine":
            date = symbol if symbol else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_contract_info_ine_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_dce":
            background_tasks.add_task(update_futures_contract_info_dce_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_czce":
            date = symbol if symbol else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_contract_info_czce_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_gfex":
            background_tasks.add_task(update_futures_contract_info_gfex_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_info_cffex":
            date = symbol if symbol else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_contract_info_cffex_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_zh_spot":
            background_tasks.add_task(update_futures_zh_spot_task, symbol, market, adjust)
            return {"success": True, "data": {"message": f"更新任务已提交 (market={market})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_zh_realtime":
            if not symbol:
                return {"success": False, "error": "更新实时行情数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_zh_realtime_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_zh_minute_sina":
            if not symbol:
                return {"success": False, "error": "更新分时行情数据需要提供 symbol 参数"}
            # 支持两种格式: 1) symbol和period独立参数, 2) symbol:period格式
            if ":" in symbol:
                sym, per = symbol.split(":", 1)
                background_tasks.add_task(update_futures_zh_minute_sina_task, sym, per)
                return {"success": True, "data": {"message": f"更新任务已提交 (symbol={sym}, period={per})", "task_id": str(uuid.uuid4())}}
            else:
                background_tasks.add_task(update_futures_zh_minute_sina_task, symbol, period)
                return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol}, period={period})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hist_em":
            if not symbol:
                return {"success": False, "error": "更新历史行情数据需要提供 symbol 参数"}
            # period参数可能是分钟周期或日周期，对于futures_hist_em，默认使用"daily"
            hist_period = period if period in ["daily", "weekly", "monthly"] else "daily"
            background_tasks.add_task(update_futures_hist_em_task, symbol, hist_period, start_date, end_date)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol}, period={hist_period})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_zh_daily_sina":
            if not symbol:
                return {"success": False, "error": "更新日频数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_zh_daily_sina_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "get_futures_daily":
            # 使用日期范围和市场参数
            background_tasks.add_task(update_get_futures_daily_task, start_date, end_date, market)
            return {"success": True, "data": {"message": f"更新任务已提交 (market={market}, date_range={start_date}-{end_date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hq_subscribe_exchange_symbol":
            background_tasks.add_task(update_futures_hq_subscribe_exchange_symbol_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_foreign_commodity_realtime":
            if not symbol:
                return {"success": False, "error": "更新外盘实时行情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_foreign_commodity_realtime_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_global_spot_em":
            background_tasks.add_task(update_futures_global_spot_em_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_global_hist_em":
            if not symbol:
                return {"success": False, "error": "更新外盘历史行情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_global_hist_em_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_foreign_hist":
            if not symbol:
                return {"success": False, "error": "更新外盘历史行情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_foreign_hist_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_foreign_detail":
            if not symbol:
                return {"success": False, "error": "更新外盘合约详情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_foreign_detail_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_settlement_price_sgx":
            date = symbol if symbol else datetime.now().strftime("%Y%m%d")
            background_tasks.add_task(update_futures_settlement_price_sgx_task, date)
            return {"success": True, "data": {"message": f"更新任务已提交 (date={date})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_main_sina":
            if not symbol:
                return {"success": False, "error": "更新连续合约需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_main_sina_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_detail":
            if not symbol:
                return {"success": False, "error": "更新合约详情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_contract_detail_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_contract_detail_em":
            if not symbol:
                return {"success": False, "error": "更新合约详情需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_contract_detail_em_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_index_ccidx":
            if not symbol:
                symbol = "中证商品期货指数"
            background_tasks.add_task(update_futures_index_ccidx_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_spot_stock":
            if not symbol:
                return {"success": False, "error": "更新现货与股票数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_spot_stock_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_comex_inventory":
            if not symbol:
                return {"success": False, "error": "更新COMEX库存数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_comex_inventory_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hog_core":
            if not symbol:
                return {"success": False, "error": "更新核心数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_hog_core_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hog_cost":
            if not symbol:
                return {"success": False, "error": "更新成本维度数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_hog_cost_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_hog_supply":
            if not symbol:
                return {"success": False, "error": "更新供应维度数据需要提供 symbol 参数"}
            background_tasks.add_task(update_futures_hog_supply_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        elif collection_name == "index_hog_spot_price":
            background_tasks.add_task(update_index_hog_spot_price_task)
            return {"success": True, "data": {"message": "更新任务已提交", "task_id": str(uuid.uuid4())}}
        elif collection_name == "futures_news_shmet":
            if not symbol:
                symbol = "全部"
            background_tasks.add_task(update_futures_news_shmet_task, symbol)
            return {"success": True, "data": {"message": f"更新任务已提交 (symbol={symbol})", "task_id": str(uuid.uuid4())}}
        
        return {"success": False, "error": f"不支持更新集合 {collection_name}"}
    except Exception as e:
        logger.error(f"提交更新任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def update_futures_fees_info_task():
    """更新期货交易费用参照表任务"""
    try:
        import akshare as ak
        logger.info("开始更新期货交易费用参照表")
        
        # 获取数据
        df = ak.futures_fees_info()
        
        if df is None or df.empty:
            logger.warning("获取期货交易费用数据为空")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_fees_info")
        
        # 批量更新
        count = 0
        for item in data:
            # 使用 合约代码 + 交易所 作为唯一标识
            key = {
                "合约代码": item.get("合约代码"), 
                "交易所": item.get("交易所")
            }
            
            # 如果没有这两个字段，跳过
            if not key["合约代码"] or not key["交易所"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"期货交易费用参照表更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新期货交易费用参照表失败: {e}", exc_info=True)


async def update_futures_delivery_dce_task(date: str):
    """更新大连商品交易所交割统计任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新大连商品交易所交割统计 (date={date})")
        
        # 获取数据
        try:
            df = ak.futures_delivery_dce(date=date)
        except Exception as e:
            logger.error(f"获取大连商品交易所交割统计失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取大连商品交易所交割统计为空 (date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_delivery_dce")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 date 字段
            item["date"] = date
            
            # 使用 date + 合约 + 交割日期 作为唯一标识
            key = {
                "date": date,
                "合约": item.get("合约"),
                "交割日期": item.get("交割日期")
            }
            
            if not key["合约"] or not key["交割日期"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"大连商品交易所交割统计更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新大连商品交易所交割统计失败: {e}", exc_info=True)


async def update_futures_delivery_czce_task(date: str):
    """更新郑州商品交易所交割统计任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新郑州商品交易所交割统计 (date={date})")
        
        # 获取数据
        try:
            df = ak.futures_delivery_czce(date=date)
        except Exception as e:
            logger.error(f"获取郑州商品交易所交割统计失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取郑州商品交易所交割统计为空 (date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_delivery_czce")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 date 字段
            item["date"] = date
            
            # 使用 date + 品种 作为唯一标识
            key = {
                "date": date,
                "品种": item.get("品种")
            }
            
            if not key["品种"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"郑州商品交易所交割统计更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新郑州商品交易所交割统计失败: {e}", exc_info=True)


async def update_futures_delivery_shfe_task(date: str):
    """更新上海期货交易所交割统计任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新上海期货交易所交割统计 (date={date})")
        
        # 获取数据
        try:
            df = ak.futures_delivery_shfe(date=date)
        except Exception as e:
            logger.error(f"获取上海期货交易所交割统计失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取上海期货交易所交割统计为空 (date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_delivery_shfe")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 date 字段
            item["date"] = date
            
            # 使用 date + 品种 作为唯一标识
            key = {
                "date": date,
                "品种": item.get("品种")
            }
            
            if not key["品种"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"上海期货交易所交割统计更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新上海期货交易所交割统计失败: {e}", exc_info=True)


async def update_futures_delivery_match_dce_task(symbol: str):
    """更新大连商品交易所交割配对任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新大连商品交易所交割配对 (symbol={symbol})")
        
        # 获取数据
        try:
            df = ak.futures_delivery_match_dce(symbol=symbol)
        except Exception as e:
            logger.error(f"获取大连商品交易所交割配对失败 (symbol={symbol}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取大连商品交易所交割配对为空 (symbol={symbol})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_delivery_match_dce")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 symbol 字段
            item["symbol"] = symbol
            
            # 使用 symbol + 合约号 + 配对日期 + 买会员号 + 卖会员号 作为唯一标识
            key = {
                "symbol": symbol,
                "合约号": item.get("合约号"),
                "配对日期": item.get("配对日期"),
                "买会员号": item.get("买会员号"),
                "卖会员号": item.get("卖会员号")
            }
            
            if not key["合约号"] or not key["配对日期"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"大连商品交易所交割配对更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新大连商品交易所交割配对失败: {e}", exc_info=True)


async def update_futures_delivery_match_czce_task(date: str):
    """更新郑州商品交易所交割配对任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新郑州商品交易所交割配对 (date={date})")
        
        # 获取数据
        try:
            df = ak.futures_delivery_match_czce(date=date)
        except Exception as e:
            logger.error(f"获取郑州商品交易所交割配对失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取郑州商品交易所交割配对为空 (date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_delivery_match_czce")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 date 字段
            item["date"] = date
            
            # 使用 date + 卖方会员 + 买方会员 作为唯一标识
            key = {
                "date": date,
                "卖方会员": item.get("卖方会员"),
                "买方会员": item.get("买方会员")
            }
            
            if not key["卖方会员"] or not key["买方会员"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"郑州商品交易所交割配对更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新郑州商品交易所交割配对失败: {e}", exc_info=True)


async def update_futures_stock_shfe_js_task(date: str):
    """更新上海期货交易所库存周报任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新上海期货交易所库存周报 (date={date})")
        
        # 获取数据
        try:
            df = ak.futures_stock_shfe_js(date=date)
        except Exception as e:
            logger.error(f"获取上海期货交易所库存周报失败 (date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取上海期货交易所库存周报为空 (date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_stock_shfe_js")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 date 字段
            item["date"] = date
            
            # 使用 date + 商品 作为唯一标识
            key = {
                "date": date,
                "商品": item.get("商品")
            }
            
            if not key["商品"]:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"上海期货交易所库存周报更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新上海期货交易所库存周报失败: {e}", exc_info=True)


async def update_futures_hold_pos_sina_task(symbol: str, contract: str, date: str):
    """更新新浪财经成交持仓任务"""
    try:
        import akshare as ak
        logger.info(f"开始更新新浪财经成交持仓 (symbol={symbol}, contract={contract}, date={date})")
        
        # 获取数据
        try:
            df = ak.futures_hold_pos_sina(symbol=symbol, contract=contract, date=date)
        except Exception as e:
            logger.error(f"获取新浪财经成交持仓失败 (symbol={symbol}, contract={contract}, date={date}): {e}")
            return
        
        if df is None or df.empty:
            logger.warning(f"获取新浪财经成交持仓为空 (symbol={symbol}, contract={contract}, date={date})")
            return

        # 转换为字典列表
        data = df.to_dict(orient="records")
        
        db = get_mongo_db()
        collection = db.get_collection("futures_hold_pos_sina")
        
        # 批量更新
        count = 0
        for item in data:
            # 增加 symbol, contract, date 字段
            item["symbol"] = symbol
            item["contract"] = contract
            item["date"] = date
            
            # 使用 symbol + contract + date + 名次 作为唯一标识
            key = {
                "symbol": symbol,
                "contract": contract,
                "date": date,
                "名次": item.get("名次")
            }
            
            if key["名次"] is None:
                continue
                
            await collection.update_one(
                key, 
                {"$set": item}, 
                upsert=True
            )
            count += 1
            
        logger.info(f"新浪财经成交持仓更新完成，共处理 {count} 条记录")
    except Exception as e:
        logger.error(f"更新新浪财经成交持仓失败: {e}", exc_info=True)
