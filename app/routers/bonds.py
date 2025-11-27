from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status, UploadFile, File, Body
from fastapi.responses import JSONResponse, FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel
import hashlib
import logging
import uuid
import asyncio
import tempfile
import os

from app.routers.auth_db import get_current_user
from tradingagents.dataflows.interface import (
    get_cn_bond_data_unified,
    get_cn_bond_info_unified,
    get_cn_bond_yield_curve_unified,
)
from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
from tradingagents.utils.instrument_validator import normalize_bond_code
from app.core.database import get_mongo_db
from app.services.bond_data_service import BondDataService
from app.services.bond_analysis_service import BondAnalysisService
from app.services.collection_refresh_service import CollectionRefreshService
from app.utils.task_manager import get_task_manager

router = APIRouter(prefix="/api/bonds", tags=["bonds"])
logger = logging.getLogger("webapi")  # 使用与其他路由一致的日志器

# 简单的内存缓存，用于减少数据库查询
_bond_list_cache = {}
_cache_ttl_seconds = 300  # 5分钟缓存

# 数据初始化锁，防止并发请求时重复从AKShare获取数据
_init_lock = asyncio.Lock()
_init_in_progress = False
_init_completed = False
_init_timestamp = None  # 初始化完成时间戳
_init_timeout_seconds = 3600  # 1小时后允许重新初始化

def _get_cache_key(q: Optional[str], category: Optional[str], exchange: Optional[str], 
                   only_not_matured: bool, page: int, page_size: int, 
                   sort_by: Optional[str], sort_dir: str) -> str:
    """生成缓存键"""
    key_str = f"{q}_{category}_{exchange}_{only_not_matured}_{page}_{page_size}_{sort_by}_{sort_dir}"
    return hashlib.md5(key_str.encode()).hexdigest()

def _is_cache_valid(cache_entry: dict) -> bool:
    """检查缓存是否有效"""
    if not cache_entry:
        return False
    cache_time = cache_entry.get("timestamp")
    if not cache_time:
        return False
    age = (datetime.now() - cache_time).total_seconds()
    return age < _cache_ttl_seconds


def _is_init_expired() -> bool:
    """检查初始化是否已过期（超时后允许重新初始化）"""
    global _init_timestamp
    if _init_timestamp is None:
        return True  # 从未初始化
    age = (datetime.now() - _init_timestamp).total_seconds()
    return age >= _init_timeout_seconds


@router.get("/list")
async def list_bonds(
    q: Optional[str] = Query(None, description="关键词过滤，按代码或名称包含匹配"),
    limit: int = Query(100, ge=1, le=1000, description="最大返回限制（兼容参数，分页优先）"),
    category: Optional[str] = Query(None, description="债券类别：convertible|exchangeable|interest|credit|other"),
    exchange: Optional[str] = Query(None, description="交易所：SH|SZ"),
    only_not_matured: bool = Query(False, description="仅显示未到期（仅对利率债生效）"),
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(20, ge=1, le=200, description="每页数量，默认20"),
    sort_by: Optional[str] = Query(None, description="排序字段：code|name|maturity_date|list_date|coupon_rate"),
    sort_dir: str = Query("asc", description="排序方向：asc/desc"),
    current_user: dict = Depends(get_current_user),
):
    try:
        logger.info(f"🔍 [债券列表] 收到请求: category={category}, page={page}, page_size={page_size}, q={q}, exchange={exchange}")
        db = get_mongo_db()
        if db is None:
            logger.error("❌ [债券列表] MongoDB数据库连接为None")
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        # 规范参数：每页最多20条；排序方向仅允许 asc/desc
        try:
            page_size = max(1, min(int(page_size), 20))
        except Exception as pe:
            logger.warning(f"⚠️ [债券列表] 参数解析失败: {pe}")
            page_size = 20
        sdir = str(sort_dir or "asc").lower()
        if sdir not in ("asc", "desc"):
            sdir = "asc"
        sort_dir = sdir
        # 如果category为空或None，不设置默认值，查询所有类别
        # 注意：这里不再强制设置默认值，让前端控制默认显示
        if category and category.strip() == "":
            category = None
        # 检查缓存
        cache_key = _get_cache_key(q, category, exchange, only_not_matured, page, page_size, sort_by, sort_dir)
        cached_result = _bond_list_cache.get(cache_key)
        
        if _is_cache_valid(cached_result):
            logger.info(f"📦 [债券列表] 从缓存获取数据 (category={category}, page={page})")
            return cached_result["data"]
        
        logger.info(f"🔧 [债券列表] 初始化BondDataService")
        svc = BondDataService(db)
        logger.info(f"🔧 [债券列表] 确保索引存在")
        try:
            await svc.ensure_indexes()
            logger.info(f"✅ [债券列表] 索引检查完成")
        except Exception as idx_err:
            logger.error(f"❌ [债券列表] 索引检查失败: {idx_err}", exc_info=True)
            # 索引失败不应该阻止查询，继续执行

        # 优先从数据库查询
        logger.info(f"🔍 [债券列表] 开始从数据库查询数据 (category={category}, page={page}, page_size={page_size}, q={q}, exchange={exchange})")
        try:
            result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)
        except TypeError as te:
            # 兼容老版本未支持排序参数的方法签名
            logger.warning(f"⚠️ [债券列表] 方法签名不匹配，尝试兼容调用: {te}")
            try:
                result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
            except TypeError:
                # 兼容更老版本未支持exchange参数的方法签名
                result = await svc.query_basic_list(q=q, category=category, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
        except Exception as e:
            logger.error(f"❌ [债券列表] 数据库查询失败: {e}", exc_info=True)
            result = {"total": 0, "items": []}

        total = int(result.get("total") or 0)
        items = list(result.get("items") or [])
        logger.info(f"📊 [债券列表] 数据库查询结果: total={total}, items={len(items)}")

        # 如果数据库中没有数据，才从 AKShare 获取并保存
        if total == 0:
            global _init_in_progress, _init_completed, _init_timestamp
            
            # 检查初始化是否已完成且未过期
            if _init_completed and not _is_init_expired():
                logger.info(f"✅ [债券列表] 初始化已完成，但category={category}无数据，返回空结果")
            elif _init_completed and _is_init_expired():
                # 初始化已过期，允许重新初始化
                logger.warning(f"⚠️ [债券列表] 初始化已过期（超过{_init_timeout_seconds}秒），将重新初始化")
                _init_completed = False
                _init_timestamp = None
            
            # 如果未初始化或已过期，执行初始化
            if not _init_completed:
                # 使用锁防止并发初始化
                async with _init_lock:
                    # 双重检查：其他请求可能已经完成初始化
                    if _init_completed:
                        logger.info(f"🔄 [债券列表] 其他请求已完成初始化，重新查询数据库")
                        try:
                            result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)
                        except TypeError:
                            try:
                                result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
                            except TypeError:
                                result = await svc.query_basic_list(q=q, category=category, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
                        total = int(result.get("total") or 0)
                        items = list(result.get("items") or [])
                    else:
                        # 第一个请求执行初始化
                        logger.warning(f"⚠️ [债券列表] 数据库为空 (total=0)，开始从 AKShare 获取数据 (category={category})")
                        _init_in_progress = True
                        
                        try:
                            provider = AKShareBondProvider()
                            fetched = await provider.get_symbol_list()
                            if fetched:
                                logger.info(f"📡 [债券列表] 从 AKShare 获取到 {len(fetched)} 条债券数据，正在保存到数据库...")
                                # 记录前几条数据的category值
                                for i, item in enumerate(fetched[:3]):
                                    logger.info(f"🔍 [债券列表] AKShare数据样本 {i+1}: code={item.get('code')}, category={item.get('category')}, name={item.get('name')}")
                                
                                saved_count = await svc.save_basic_list(fetched)
                                logger.info(f"💾 [债券列表] 已保存 {saved_count} 条债券数据到数据库")
                                
                                # 验证：先不带category条件查询，看看数据是否存在
                                try:
                                    test_result = await svc.query_basic_list(q=None, category=None, exchange=exchange, only_not_matured=False, page=1, page_size=5, sort_by=None, sort_dir="asc")
                                    logger.info(f"🔍 [债券列表] 验证查询（无category过滤）: total={test_result.get('total', 0)}, items={len(test_result.get('items', []))}")
                                    if test_result.get('items'):
                                        sample = test_result['items'][0]
                                        logger.info(f"🔍 [债券列表] 数据库样本数据: code={sample.get('code')}, category={sample.get('category')}, name={sample.get('name')}")
                                except Exception as test_err:
                                    logger.error(f"❌ [债券列表] 验证查询失败: {test_err}")
                                
                                # 标记初始化完成，记录时间戳
                                _init_completed = True
                                _init_timestamp = datetime.now()
                                logger.info(f"✅ [债券列表] 数据初始化完成，时间戳: {_init_timestamp}")
                                
                                # 重新查询数据库
                                try:
                                    result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)
                                except TypeError:
                                    # 兼容老版本未支持排序参数的方法签名
                                    try:
                                        result = await svc.query_basic_list(q=q, category=category, exchange=exchange, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
                                    except TypeError:
                                        # 兼容更老版本未支持exchange参数的方法签名
                                        result = await svc.query_basic_list(q=q, category=category, only_not_matured=only_not_matured, page=page, page_size=page_size)  # type: ignore
                                total = int(result.get("total") or 0)
                                items = list(result.get("items") or [])
                                logger.info(f"✅ [债券列表] 保存后重新查询数据库: total={total}, items={len(items)}")
                            else:
                                logger.warning(f"⚠️ [债券列表] 从 AKShare 获取数据为空")
                                _init_completed = True  # 即使为空也标记完成，避免重复尝试
                                _init_timestamp = datetime.now()  # 记录时间戳，超时后可重试
                        except Exception as e:
                            logger.error(f"❌ [债券列表] 从 AKShare 获取数据失败: {e}", exc_info=True)
                            _init_completed = True  # 失败也标记完成，避免无限重试
                            _init_timestamp = datetime.now()  # 记录时间戳，超时后可重试
                        finally:
                            _init_in_progress = False
        else:
            logger.info(f"✅ [债券列表] 从数据库获取 {total} 条债券数据 (category={category}, page={page}, items={len(items)})")

        # 移除 _id 和 ObjectId，避免序列化问题
        from bson import ObjectId
        from datetime import datetime as dt, date
        logger.info(f"🔧 [债券列表] 开始处理 {len(items)} 条数据的序列化")
        for idx, it in enumerate(items):
            try:
                if isinstance(it, dict):
                    # 移除 _id 字段
                    if "_id" in it:
                        it.pop("_id", None)
                    # 确保所有字段都是可序列化的
                    for key, value in list(it.items()):
                        if value is None:
                            continue
                        # 处理 ObjectId
                        if isinstance(value, ObjectId):
                            it[key] = str(value)
                        # 处理 datetime 和 date
                        elif isinstance(value, (dt, date)):
                            it[key] = value.isoformat()
                        # 处理其他不可序列化的类型
                        elif not isinstance(value, (str, int, float, bool, list, dict)):
                            try:
                                it[key] = str(value)
                            except Exception:
                                it.pop(key, None)
                        # 处理嵌套字典中的 ObjectId 和 datetime
                        elif isinstance(value, dict):
                            for k, v in list(value.items()):
                                if isinstance(v, ObjectId):
                                    value[k] = str(v)
                                elif isinstance(v, (dt, date)):
                                    value[k] = v.isoformat()
                        # 处理列表中的 ObjectId 和 datetime
                        elif isinstance(value, list):
                            for i, v in enumerate(value):
                                if isinstance(v, ObjectId):
                                    value[i] = str(v)
                                elif isinstance(v, (dt, date)):
                                    value[i] = v.isoformat()
                                elif isinstance(v, dict):
                                    for k, v2 in list(v.items()):
                                        if isinstance(v2, ObjectId):
                                            v[k] = str(v2)
                                        elif isinstance(v2, (dt, date)):
                                            v[k] = v2.isoformat()
            except Exception as ser_err:
                logger.error(f"❌ [债券列表] 序列化第 {idx} 条数据失败: {ser_err}", exc_info=True)
                # 如果某条数据序列化失败，尝试移除问题字段或跳过
                try:
                    # 尝试将所有字段转为字符串
                    for k, v in list(it.items()):
                        try:
                            if not isinstance(v, (str, int, float, bool, list, dict)):
                                it[k] = str(v)
                        except:
                            it.pop(k, None)
                except:
                    # 如果还是失败，从列表中移除这条数据
                    logger.warning(f"⚠️ [债券列表] 移除无法序列化的数据项 {idx}")
                    items[idx] = None
        # 移除 None 项
        items = [it for it in items if it is not None]
        logger.info(f"✅ [债券列表] 序列化完成，剩余 {len(items)} 条数据")

        # 兼容 limit（若调用方仍传入limit，则仍然生效于当前页上限）
        if limit and len(items) > limit:
            items = items[:limit]

        # 构建返回数据
        logger.info(f"🔧 [债券列表] 构建响应数据: total={total}, items_count={len(items)}")
        try:
            response_data = {"success": True, "data": {"total": total, "page": page, "page_size": page_size, "items": items}}
            logger.info(f"✅ [债券列表] 响应数据构建成功")
        except Exception as build_err:
            logger.error(f"❌ [债券列表] 构建响应数据失败: {build_err}", exc_info=True)
            raise
        
        # 缓存结果（只缓存数据库中有数据的情况，避免缓存空结果）
        if total > 0:
            try:
                _bond_list_cache[cache_key] = {
                    "data": response_data,
                    "timestamp": datetime.now()
                }
                # 清理过期缓存（保持缓存大小合理）
                if len(_bond_list_cache) > 1000:
                    now = datetime.now()
                    expired_keys = [k for k, v in _bond_list_cache.items() 
                                  if not _is_cache_valid(v)]
                    for k in expired_keys:
                        _bond_list_cache.pop(k, None)
            except Exception as cache_err:
                logger.warning(f"⚠️ [债券列表] 缓存操作失败: {cache_err}")

        logger.info(f"✅ [债券列表] 请求处理完成，返回数据")
        return response_data
    except HTTPException:
        # HTTPException应该直接抛出，不要捕获
        raise
    except Exception as e:
        logger.error(f"❌ [债券列表] 处理请求时发生错误: {e}", exc_info=True)
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"❌ [债券列表] 错误堆栈: {error_trace}")
        # 确保变量已定义
        try:
            page_val = page
        except:
            page_val = 1
        try:
            page_size_val = page_size
        except:
            page_size_val = 20
        # 抛出HTTPException，让全局异常处理器处理
        raise HTTPException(
            status_code=500,
            detail=f"获取债券列表失败: {str(e)}"
        )


@router.get("/{code}/history")
async def get_bond_history(
    code: str,
    start: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end: str = Query(..., description="结束日期 YYYY-MM-DD"),
    period: str = Query("daily", description="周期，默认 daily"),
    current_user: dict = Depends(get_current_user),
):
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    
    # 优先从数据库查询历史数据
    df = await svc.query_bond_daily(code, start, end)
    
    # 如果数据库中没有数据或数据不完整，从接口获取并保存
    if df is None or df.empty:
        # 从接口获取数据
        result = get_cn_bond_data_unified(code, start, end, period)
        
        # 如果接口返回成功，尝试保存到数据库
        if not result.startswith("❌") and not result.startswith("⚠️"):
            try:
                # 使用provider直接获取DataFrame以便保存
                provider = AKShareBondProvider()
                norm = normalize_bond_code(code)
                code_std = norm.get("code_std") or code
                
                # 获取历史数据
                hist_df = await provider.get_historical_data(code_std, start, end, period)
                if hist_df is not None and not hist_df.empty:
                    # 保存到数据库
                    await svc.save_bond_daily(code_std, hist_df)
            except Exception as e:
                # 保存失败不影响返回数据
                import logging
                logging.warning(f"保存债券历史数据到数据库失败: {e}")
        
        return {"success": not result.startswith("❌"), "data": result}
    else:
        # 数据库中有数据，转换为字符串格式返回（与接口格式保持一致）
        try:
            preview = df.to_string(index=False)
            title = f"## 债券 {code} 历史数据 ({start} 到 {end})"
            result = f"{title}\n" + preview
            return {"success": True, "data": result, "from_db": True}
        except Exception as e:
            # 转换失败，回退到接口
            result = get_cn_bond_data_unified(code, start, end, period)
            return {"success": not result.startswith("❌"), "data": result}


@router.get("/{code}/analytics")
async def get_bond_analytics(
    code: str,
    start: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end: str = Query(..., description="结束日期 YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user),
):
    # 现阶段的分析结果随历史数据字符串一起包含（含MA/MACD/RSI/BOLL等），先复用历史数据接口
    # 优先从数据库查询历史数据
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    
    df = await svc.query_bond_daily(code, start, end)
    
    # 如果数据库中没有数据或数据不完整，从接口获取并保存
    if df is None or df.empty:
        # 从接口获取数据
        result = get_cn_bond_data_unified(code, start, end, period="daily")
        
        # 如果接口返回成功，尝试保存到数据库
        if not result.startswith("❌") and not result.startswith("⚠️"):
            try:
                # 使用provider直接获取DataFrame以便保存
                provider = AKShareBondProvider()
                norm = normalize_bond_code(code)
                code_std = norm.get("code_std") or code
                
                # 获取历史数据
                hist_df = await provider.get_historical_data(code_std, start, end, period="daily")
                if hist_df is not None and not hist_df.empty:
                    # 保存到数据库
                    await svc.save_bond_daily(code_std, hist_df)
            except Exception as e:
                # 保存失败不影响返回数据
                import logging
                logging.warning(f"保存债券历史数据到数据库失败: {e}")
        
        return {"success": not result.startswith("❌"), "data": result}
    else:
        # 数据库中有数据，转换为字符串格式返回（与接口格式保持一致）
        try:
            preview = df.to_string(index=False)
            title = f"## 债券 {code} 历史数据与分析 ({start} 到 {end})"
            result = f"{title}\n" + preview
            return {"success": True, "data": result, "from_db": True}
        except Exception as e:
            # 转换失败，回退到接口
            result = get_cn_bond_data_unified(code, start, end, period="daily")
            return {"success": not result.startswith("❌"), "data": result}


@router.get("/{code}/info")
async def get_bond_info(
    code: str,
    current_user: dict = Depends(get_current_user),
):
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    
    # 优先从数据库查询详情信息
    info = await svc.query_bond_info(code)
    
    # 如果数据库中没有，从接口获取并保存
    if not info or (isinstance(info, dict) and info.get("error")):
        info = get_cn_bond_info_unified(code)
        
        # 如果接口返回的数据格式不对，尝试从基础列表获取
        if isinstance(info, dict) and info.get("error"):
            # 从基础列表中查找
            try:
                result = await svc.query_basic_list(q=code, page=1, page_size=1)
                items = result.get("items", [])
                if items and len(items) > 0:
                    info = items[0]
                    info.pop("_id", None)
            except Exception:
                pass
        
        # 处理接口返回的格式（如果是嵌套的data字段）
        if isinstance(info, dict) and "data" in info and isinstance(info.get("data"), list) and len(info.get("data", [])) > 0:
            # 将data中的第一条记录展开
            data_records = info.get("data", [])
            if data_records:
                # 保留code和source等字段，合并data中的字段
                code_value = info.get("code", code)
                source_value = info.get("source", "akshare")
                data_item = data_records[0]
                info = {"code": code_value, "source": source_value}
                info.update(data_item)
        
        # 如果成功获取到数据且没有错误，保存到数据库
        if isinstance(info, dict) and not info.get("error"):
            try:
                await svc.save_bond_info_from_api(code, info)
            except Exception as e:
                # 保存失败不影响返回数据
                import logging
                logging.warning(f"保存债券详情到数据库失败: {e}")
    
    ok = isinstance(info, dict) and not info.get("error")
    return {"success": ok, "data": info}


@router.get("/yield-curve")
async def get_bond_yield_curve(
    start: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD，可选"),
    end: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD，可选"),
    curve_name: Optional[str] = Query(None, description="曲线名称，可选"),
    format: str = Query("json", description="返回格式：json|text"),
    current_user: dict = Depends(get_current_user),
):
    """获取收益率曲线数据，支持JSON和文本两种格式"""
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    
    # 优先从数据库查询收益率曲线数据
    df = await svc.query_yield_curve(start, end, curve_name)
    
    # 如果数据库中没有数据或数据不完整，从接口获取并保存
    if df is None or df.empty:
        # 从接口获取数据
        result = get_cn_bond_yield_curve_unified(start, end)
        
        # 如果接口返回成功，尝试保存到数据库
        if not result.startswith("❌") and not result.startswith("⚠️"):
            try:
                # 使用provider直接获取DataFrame以便保存
                provider = AKShareBondProvider()
                yield_df = await provider.get_yield_curve(start_date=start, end_date=end)
                if yield_df is not None and not yield_df.empty:
                    # 保存到数据库
                    await svc.save_yield_curve(yield_df)
                    # 重新查询数据库
                    df = await svc.query_yield_curve(start, end, curve_name)
            except Exception as e:
                # 保存失败不影响返回数据
                import logging
                logging.warning(f"保存收益率曲线数据到数据库失败: {e}")
        
        # 如果仍然没有数据，返回文本格式
        if format == "text":
            return {"success": not result.startswith("❌"), "data": result}
        else:
            return {"success": False, "data": [], "message": "无数据"}
    else:
        # 数据库中有数据
        if format == "text":
            # 文本格式（兼容旧接口）
            try:
                preview = df.to_string(index=False)
                rng = f"{start or '-∞'} 到 {end or '+∞'}"
                title = f"## 中国债券收益率曲线 ({rng})"
                result = f"{title}\n" + preview
                return {"success": True, "data": result, "from_db": True}
            except Exception as e:
                # 转换失败，回退到接口
                result = get_cn_bond_yield_curve_unified(start, end)
                return {"success": not result.startswith("❌"), "data": result}
        else:
            # JSON格式（新格式，用于前端图表）
            try:
                # 转换为字典列表
                records = df.to_dict(orient="records")
                
                # 获取统计信息
                curve_names = df["curve_name"].unique().tolist() if "curve_name" in df.columns else []
                tenors = sorted(df["tenor"].unique().tolist()) if "tenor" in df.columns else []
                dates = sorted(df["date"].unique().tolist()) if "date" in df.columns else []
                
                # 按日期和期限组织数据，便于图表展示
                chart_data = {}
                for record in records:
                    date = record.get("date")
                    tenor = record.get("tenor")
                    curve = record.get("curve_name") or "default"
                    yield_val = record.get("yield")
                    
                    if date not in chart_data:
                        chart_data[date] = {}
                    if curve not in chart_data[date]:
                        chart_data[date][curve] = {}
                    chart_data[date][curve][tenor] = yield_val
                
                return {
                    "success": True,
                    "data": {
                        "records": records,
                        "chart_data": chart_data,
                        "statistics": {
                            "total_records": len(records),
                            "curve_names": curve_names,
                            "tenors": tenors,
                            "date_range": {
                                "start": dates[0] if dates else None,
                                "end": dates[-1] if dates else None,
                                "count": len(dates)
                            }
                        }
                    },
                    "from_db": True
                }
            except Exception as e:
                logger.error(f"转换收益率曲线数据失败: {e}", exc_info=True)
                return {"success": False, "error": str(e)}


@router.post("/yield-curve/sync")
async def sync_bond_yield_curve(
    start: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD，可选"),
    end: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD，可选"),
    current_user: dict = Depends(get_current_user),
):
    provider = AKShareBondProvider()
    df = await provider.get_yield_curve(start, end)
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    saved = await svc.save_yield_curve(df)
    return {"success": True, "data": {"saved": saved, "rows": 0 if df is None else len(df)}}


@router.get("/collections")
async def list_bond_collections(
    current_user: dict = Depends(get_current_user),
):
    """获取所有债券相关数据集合列表及其说明"""
    collections = [
        # 01 基础数据
        {
            "name": "bond_info_cm",
            "display_name": "债券信息查询",
            "description": "中国外汇交易中心债券信息查询，支持按债券名称、代码、发行人、债券类型、付息方式、发行年份、承销商、评级等条件查询",
            "route": "/bonds/collections/bond_info_cm",
            "source": "中国外汇交易中心",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "基础数据",
        },
        # 02
        {
            "name": "bond_info_detail_cm",
            "display_name": "债券基础信息",
            "description": "债券详细信息，包括发行条款、评级等详细数据",
            "route": "/bonds/collections/bond_info_detail_cm",
            "source": "中国外汇交易中心",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "基础数据",
        },
        # 03 沪深债券行情
        {
            "name": "bond_zh_hs_spot",
            "display_name": "沪深债券实时行情",
            "description": "沪深债券实时行情数据，包括最新价、涨跌幅、成交量等",
            "route": "/bonds/collections/bond_zh_hs_spot",
            "source": "新浪财经",
            "priority": "⭐⭐⭐⭐",
            "category": "沪深债券行情",
        },
        # 04
        {
            "name": "bond_zh_hs_daily",
            "display_name": "沪深债券历史行情",
            "description": "沪深债券历史行情数据（日线），支持按日期查询",
            "route": "/bonds/collections/bond_zh_hs_daily",
            "source": "新浪财经",
            "priority": "⭐⭐⭐⭐",
            "category": "沪深债券行情",
        },
        # 05 可转债行情数据
        {
            "name": "bond_zh_hs_cov_spot",
            "display_name": "可转债实时行情",
            "description": "沪深可转债实时行情数据",
            "route": "/bonds/collections/bond_zh_hs_cov_spot",
            "source": "新浪财经",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "可转债行情",
        },
        # 06
        {
            "name": "bond_zh_hs_cov_daily",
            "display_name": "可转债历史行情",
            "description": "沪深可转债历史行情数据（日线）",
            "route": "/bonds/collections/bond_zh_hs_cov_daily",
            "source": "新浪财经",
            "priority": "⭐⭐⭐⭐",
            "category": "可转债行情",
        },
        # 07
        {
            "name": "bond_zh_cov",
            "display_name": "可转债数据一览表",
            "description": "可转债综合数据，包括申购、转股价、溢价率等",
            "route": "/bonds/collections/bond_zh_cov",
            "source": "东方财富网",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "可转债行情",
        },
        # 08 市场概览数据
        {
            "name": "bond_cash_summary_sse",
            "display_name": "债券现券市场概览",
            "description": "上交所债券现券市场托管概览",
            "route": "/bonds/collections/bond_cash_summary_sse",
            "source": "上海证券交易所",
            "priority": "⭐⭐⭐",
            "category": "市场概览",
        },
        # 09
        {
            "name": "bond_deal_summary_sse",
            "display_name": "债券成交概览",
            "description": "上交所债券成交概览",
            "route": "/bonds/collections/bond_deal_summary_sse",
            "source": "上海证券交易所",
            "priority": "⭐⭐⭐",
            "category": "市场概览",
        },
        # 10 银行间市场
        {
            "name": "bond_debt_nafmii",
            "display_name": "银行间市场债券发行",
            "description": "银行间市场债券发行基础数据",
            "route": "/bonds/collections/bond_debt_nafmii",
            "source": "中国银行间市场交易商协会",
            "priority": "⭐⭐⭐",
            "category": "银行间市场",
        },
        # 11
        {
            "name": "bond_spot_quote",
            "display_name": "现券市场做市报价",
            "description": "银行间现券市场做市报价",
            "route": "/bonds/collections/bond_spot_quote",
            "source": "中国外汇交易中心",
            "priority": "⭐⭐⭐",
            "category": "银行间市场",
        },
        # 12
        {
            "name": "bond_spot_deal",
            "display_name": "现券市场成交行情",
            "description": "银行间现券市场成交行情",
            "route": "/bonds/collections/bond_spot_deal",
            "source": "中国外汇交易中心",
            "priority": "⭐⭐⭐",
            "category": "银行间市场",
        },
        # 13 可转债分时
        {
            "name": "bond_zh_hs_cov_min",
            "display_name": "可转债分时行情",
            "description": "可转债分时行情数据，支持多周期",
            "route": "/bonds/collections/bond_zh_hs_cov_min",
            "source": "东方财富网",
            "priority": "⭐⭐⭐",
            "category": "可转债行情",
        },
        # 14
        {
            "name": "bond_zh_hs_cov_pre_min",
            "display_name": "可转债盘前分时",
            "description": "可转债盘前分时数据",
            "route": "/bonds/collections/bond_zh_hs_cov_pre_min",
            "source": "东方财富网",
            "priority": "⭐⭐",
            "category": "可转债行情",
        },
        # 15 可转债详细数据
        {
            "name": "bond_zh_cov_info",
            "display_name": "可转债详情-东财",
            "description": "可转债详情（基本信息、中签号、筹资用途、重要日期）",
            "route": "/bonds/collections/bond_zh_cov_info",
            "source": "东方财富网",
            "priority": "⭐⭐⭐⭐",
            "category": "可转债详细",
        },
        # 16
        {
            "name": "bond_zh_cov_info_ths",
            "display_name": "可转债详情-同花顺",
            "description": "可转债详情（同花顺数据源）",
            "route": "/bonds/collections/bond_zh_cov_info_ths",
            "source": "同花顺",
            "priority": "⭐⭐⭐",
            "category": "可转债详细",
        },
        # 17
        {
            "name": "bond_cov_comparison",
            "display_name": "可转债比价表",
            "description": "可转债与正股比价数据",
            "route": "/bonds/collections/bond_cov_comparison",
            "source": "东方财富网",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "可转债详细",
        },
        # 18
        {
            "name": "bond_zh_cov_value_analysis",
            "display_name": "可转债价值分析",
            "description": "可转债价值分析（纯债价值、转股价值、溢价率）",
            "route": "/bonds/collections/bond_zh_cov_value_analysis",
            "source": "东方财富网",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "可转债详细",
        },
        # 19 质押式回购
        {
            "name": "bond_sh_buy_back_em",
            "display_name": "上证质押式回购",
            "description": "上证质押式回购实时行情",
            "route": "/bonds/collections/bond_sh_buy_back_em",
            "source": "东方财富网",
            "priority": "⭐⭐⭐",
            "category": "质押式回购",
        },
        # 20
        {
            "name": "bond_sz_buy_back_em",
            "display_name": "深证质押式回购",
            "description": "深证质押式回购实时行情",
            "route": "/bonds/collections/bond_sz_buy_back_em",
            "source": "东方财富网",
            "priority": "⭐⭐⭐",
            "category": "质押式回购",
        },
        # 21
        {
            "name": "bond_buy_back_hist_em",
            "display_name": "质押式回购历史数据",
            "description": "质押式回购历史行情",
            "route": "/bonds/collections/bond_buy_back_hist_em",
            "source": "东方财富网",
            "priority": "⭐⭐⭐",
            "category": "质押式回购",
        },
        # 22 集思录数据
        {
            "name": "bond_cb_jsl",
            "display_name": "可转债实时数据-集思录",
            "description": "集思录可转债实时数据（需要Cookie）",
            "route": "/bonds/collections/bond_cb_jsl",
            "source": "集思录",
            "priority": "⭐⭐⭐⭐⭐",
            "category": "集思录数据",
        },
        # 23
        {
            "name": "bond_cb_redeem_jsl",
            "display_name": "可转债强赎-集思录",
            "description": "可转债强赎信息",
            "route": "/bonds/collections/bond_cb_redeem_jsl",
            "source": "集思录",
            "priority": "⭐⭐⭐⭐",
            "category": "集思录数据",
        },
        # 24
        {
            "name": "bond_cb_index_jsl",
            "display_name": "可转债等权指数-集思录",
            "description": "集思录可转债等权指数",
            "route": "/bonds/collections/bond_cb_index_jsl",
            "source": "集思录",
            "priority": "⭐⭐⭐",
            "category": "集思录数据",
        },
        # 25
        {
            "name": "bond_cb_adj_logs_jsl",
            "display_name": "转股价调整记录-集思录",
            "description": "可转债转股价调整记录",
            "route": "/bonds/collections/bond_cb_adj_logs_jsl",
            "source": "集思录",
            "priority": "⭐⭐⭐",
            "category": "集思录数据",
        },
        # 26 收益率曲线
        {
            "name": "bond_china_close_return",
            "display_name": "收益率曲线历史数据",
            "description": "中国债券收益率曲线历史数据",
            "route": "/bonds/collections/bond_china_close_return",
            "source": "中国外汇交易中心",
            "priority": "⭐⭐⭐",
            "category": "收益率曲线",
        },
        # 27
        {
            "name": "bond_zh_us_rate",
            "display_name": "中美国债收益率",
            "description": "中美国债收益率对比数据",
            "route": "/bonds/collections/bond_zh_us_rate",
            "source": "东方财富网",
            "priority": "⭐⭐⭐",
            "category": "收益率曲线",
        },
        # 28 债券发行数据
        {
            "name": "bond_treasure_issue_cninfo",
            "display_name": "国债发行",
            "description": "国债发行信息",
            "route": "/bonds/collections/bond_treasure_issue_cninfo",
            "source": "巨潮资讯",
            "priority": "⭐⭐",
            "category": "债券发行",
        },
        # 29
        {
            "name": "bond_local_government_issue_cninfo",
            "display_name": "地方债发行",
            "description": "地方债发行信息",
            "route": "/bonds/collections/bond_local_government_issue_cninfo",
            "source": "巨潮资讯",
            "priority": "⭐⭐",
            "category": "债券发行",
        },
        # 30
        {
            "name": "bond_corporate_issue_cninfo",
            "display_name": "企业债发行",
            "description": "企业债发行信息",
            "route": "/bonds/collections/bond_corporate_issue_cninfo",
            "source": "巨潮资讯",
            "priority": "⭐⭐",
            "category": "债券发行",
        },
        # 31
        {
            "name": "bond_cov_issue_cninfo",
            "display_name": "可转债发行",
            "description": "可转债发行信息",
            "route": "/bonds/collections/bond_cov_issue_cninfo",
            "source": "巨潮资讯",
            "priority": "⭐⭐⭐",
            "category": "债券发行",
        },
        # 32
        {
            "name": "bond_cov_stock_issue_cninfo",
            "display_name": "可转债转股",
            "description": "可转债转股信息",
            "route": "/bonds/collections/bond_cov_stock_issue_cninfo",
            "source": "巨潮资讯",
            "priority": "⭐⭐⭐",
            "category": "债券发行",
        },
        # 33 中债指数
        {
            "name": "bond_new_composite_index_cbond",
            "display_name": "中债新综合指数",
            "description": "中债新综合指数",
            "route": "/bonds/collections/bond_new_composite_index_cbond",
            "source": "中国债券信息网",
            "priority": "⭐⭐",
            "category": "中债指数",
        },
        # 34
        {
            "name": "bond_composite_index_cbond",
            "display_name": "中债综合指数",
            "description": "中债综合指数",
            "route": "/bonds/collections/bond_composite_index_cbond",
            "source": "中国债券信息网",
            "priority": "⭐⭐",
            "category": "中债指数",
        },
    ]
    return {"success": True, "data": collections}


@router.get("/collections/{collection_name}/update-config")
async def get_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定集合的更新配置信息
    
    返回该集合支持的单条更新和批量更新参数配置
    """
    from app.config.bond_update_config import get_collection_update_config as get_config
    config = get_config(collection_name)
    return {"success": True, "data": config}


@router.get("/collections/{collection_name}")
async def get_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量，默认50"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: dict = Depends(get_current_user),
):
    """获取指定集合的数据（分页）"""
    db = get_mongo_db()
    svc = BondDataService(db)
    
    # 映射所有34个债券数据集合到对应的MongoDB集合
    collection_map = {
        # 01-02 基础数据
        "bond_info_cm": svc.col_info_cm,
        "bond_info_detail_cm": svc.col_basic,
        # 03-04 沪深债券行情
        "bond_zh_hs_spot": svc.col_zh_hs_spot,
        "bond_zh_hs_daily": svc.col_zh_hs_daily,
        # 05-07 可转债行情
        "bond_zh_hs_cov_spot": svc.col_zh_hs_cov_spot,
        "bond_zh_hs_cov_daily": svc.col_zh_hs_cov_daily,
        "bond_zh_cov": svc.col_zh_cov,
        # 08-09 市场概览
        "bond_cash_summary_sse": svc.col_cash_summary_sse,
        "bond_deal_summary_sse": svc.col_deal_summary_sse,
        # 10-12 银行间市场
        "bond_debt_nafmii": svc.col_debt_nafmii,
        "bond_spot_quote": svc.col_spot_quote,
        "bond_spot_deal": svc.col_spot_deal,
        # 13-14 可转债分时
        "bond_zh_hs_cov_min": svc.col_zh_hs_cov_min,
        "bond_zh_hs_cov_pre_min": svc.col_zh_hs_cov_pre_min,
        # 15-18 可转债详细
        "bond_zh_cov_info": svc.col_zh_cov_info,
        "bond_zh_cov_info_ths": svc.col_zh_cov_info_ths,
        "bond_cov_comparison": svc.col_cov_comparison,
        "bond_zh_cov_value_analysis": svc.col_zh_cov_value_analysis,
        # 19-21 质押式回购
        "bond_sh_buy_back_em": svc.col_sh_buy_back,
        "bond_sz_buy_back_em": svc.col_sz_buy_back,
        "bond_buy_back_hist_em": svc.col_buybacks_hist,
        # 22-25 集思录数据
        "bond_cb_jsl": svc.col_cov_jsl,
        "bond_cb_redeem_jsl": svc.col_cov_redeem_jsl,
        "bond_cb_index_jsl": svc.col_cov_index_jsl,
        "bond_cb_adj_logs_jsl": svc.col_cov_adj_jsl,
        # 26-27 收益率曲线
        "bond_china_close_return": svc.col_yield_curve_hist,
        "bond_zh_us_rate": svc.col_cn_us_yield,
        # 28-32 债券发行
        "bond_treasure_issue_cninfo": svc.col_treasury_issue,
        "bond_local_government_issue_cninfo": svc.col_local_issue,
        "bond_corporate_issue_cninfo": svc.col_corporate_issue,
        "bond_cov_issue_cninfo": svc.col_cov_issue,
        "bond_cov_stock_issue_cninfo": svc.col_cov_convert,
        # 33-34 中债指数
        "bond_new_composite_index_cbond": svc.col_zh_bond_new_index,
        "bond_composite_index_cbond": svc.col_zh_bond_index,
    }
    
    collection = collection_map.get(collection_name)
    if collection is None:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    
    try:
        # 构建查询条件
        query = {}
        
        # 对于 bond_info_cm 集合，只查询标准数据记录，不查询详细查询记录
        # 这样可以确保列表页面不会显示详细查询数据（60+个英文字段）
        if collection_name == "bond_info_cm":
            query["endpoint"] = "bond_info_cm"
        
        # 安全检查：确保 filter_field 和 filter_value 都是字符串且非空
        # 注意：需要先检查类型，避免对Collection对象进行布尔运算
        # 使用try-except和type()检查，完全避免布尔运算
        try:
            # 先检查类型，使用type()而不是isinstance()以避免布尔运算
            # 必须先检查类型，不能先进行布尔运算（包括or表达式）
            filter_field_type = type(filter_field) if filter_field is not None else None
            filter_value_type = type(filter_value) if filter_value is not None else None
            
            # 只有当两个参数都是字符串类型时才处理
            if filter_field_type is str and filter_value_type is str:
                # 现在可以安全地调用strip()
                filter_field_stripped = filter_field.strip()
                filter_value_stripped = filter_value.strip()
                # 检查strip后的结果是否为空（字符串可以直接进行布尔运算）
                if filter_field_stripped and filter_value_stripped:
                    # 支持模糊查询
                    if filter_field_stripped in ["code", "name", "债券简称", "债券代码"]:
                        query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                    else:
                        query[filter_field_stripped] = filter_value_stripped
        except (AttributeError, NotImplementedError, TypeError) as filter_err:
            # 如果filter_field或filter_value不是字符串类型（可能是Collection对象），忽略过滤
            logger.warning(f"⚠️ [集合数据] 过滤参数无效，将忽略: {filter_err}")
            pass
        
        # 获取总数
        total = await collection.count_documents(query)
        
        # 构建排序
        # 默认按日期倒序，如果没有日期字段则按_id倒序
        default_sort_key = None
        for date_field in ["date", "datetime", "timestamp", "更新日期", "发行日期", "上市日期"]:
            # 检查集合中是否有该字段的文档
            test_doc = await collection.find_one({date_field: {"$exists": True}})
            if test_doc is not None:
                default_sort_key = date_field
                break
        
        # 显式选择排序键，避免使用 or 链引发的隐式布尔求值
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
        items = []
        
        async for doc in cursor:
            # 移除 _id 或转换为字符串
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)
        
        # 获取字段信息（从当前页的记录收集）
        # 所有页面使用统一的字段收集逻辑
        fields_info = []
        if items:
            field_map = {}  # {field_name: {"type": str, "example": str}}
            
            # 从当前页的所有记录收集字段
            for item in items:
                # 对于 bond_info_cm 集合，只从标准数据记录收集字段，忽略详细查询记录
                # bond_info_cm 集合包含两种数据：
                # - 标准数据（endpoint="bond_info_cm"）: 10个中文字段，用于列表显示
                # - 详细查询数据（endpoint="bond_info_cm_query"）: 60+个英文字段，用于详情页
                # 为了保证第一页和第二页显示一致，只从标准数据收集字段
                if collection_name == "bond_info_cm":
                    item_endpoint = item.get("endpoint", "")
                    if item_endpoint != "bond_info_cm":
                        # 跳过详细查询记录，不从中收集字段
                        continue
                
                for key, value in item.items():
                    if key != "_id" and key not in field_map:
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
                        
                        field_map[key] = {
                            "name": key,
                            "type": field_type,
                            "example": str(value)[:50] if value is not None else None,
                        }
            
            # 转换为列表
            fields_info = list(field_map.values())
        
        # 对于 bond_info_cm 集合，只显示标准字段（中文字段），忽略详细查询的英文字段
        if collection_name == "bond_info_cm" and fields_info:
            # 定义标准显示字段（按显示顺序）
            standard_fields = [
                "债券代码",
                "债券简称", 
                "债券类型",
                "发行人/受托机构",
                "发行日期",
                "最新债项评级",
                "查询代码",
                "endpoint",
                "code",
                "source"
            ]
            
            # 只保留标准字段（按定义的顺序）
            ordered_fields = []
            field_dict = {f["name"]: f for f in fields_info}
            
            for field_name in standard_fields:
                if field_name in field_dict:
                    ordered_fields.append(field_dict[field_name])
            
            # 如果标准字段不存在（可能是新数据），保留所有中文字段
            if len(ordered_fields) < 5:
                logger.warning(f"⚠️ [集合数据] bond_info_cm未找到标准字段，使用所有中文字段")
                # 分离中文字段和其他字段
                chinese_fields = [f for f in fields_info if any('\u4e00' <= c <= '\u9fff' for c in f["name"])]
                meta_fields = [f for f in fields_info if f["name"] in ["endpoint", "code", "source"]]
                ordered_fields = chinese_fields + meta_fields
            
            fields_info = ordered_fields
            logger.info(f"✅ [集合数据] bond_info_cm显示{len(fields_info)}个标准字段")
        
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
        logger.error(f"获取集合 {collection_name} 数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定集合的统计信息"""
    db = get_mongo_db()
    svc = BondDataService(db)
    
    # 映射所有债券数据集合到对应的MongoDB集合（包含34个主要集合和其他辅助集合）
    collection_map = {
        # 01-02 基础数据
        "bond_info_cm": svc.col_info_cm,
        "bond_info_detail_cm": svc.col_basic,
        # 03-04 沪深债券行情
        "bond_zh_hs_spot": svc.col_zh_hs_spot,
        "bond_zh_hs_daily": svc.col_zh_hs_daily,
        # 05-07 可转债行情
        "bond_zh_hs_cov_spot": svc.col_zh_hs_cov_spot,
        "bond_zh_hs_cov_daily": svc.col_zh_hs_cov_daily,
        "bond_zh_cov": svc.col_zh_cov,
        # 08-09 市场概览
        "bond_cash_summary_sse": svc.col_cash_summary_sse,
        "bond_deal_summary_sse": svc.col_deal_summary_sse,
        # 10-12 银行间市场
        "bond_debt_nafmii": svc.col_debt_nafmii,
        "bond_spot_quote": svc.col_spot_quote,
        "bond_spot_deal": svc.col_spot_deal,
        # 13-14 可转债分时
        "bond_zh_hs_cov_min": svc.col_zh_hs_cov_min,
        "bond_zh_hs_cov_pre_min": svc.col_zh_hs_cov_pre_min,
        # 15-18 可转债详细
        "bond_zh_cov_info": svc.col_zh_cov_info,
        "bond_zh_cov_info_ths": svc.col_zh_cov_info_ths,
        "bond_cov_comparison": svc.col_cov_comparison,
        "bond_zh_cov_value_analysis": svc.col_zh_cov_value_analysis,
        # 19-21 质押式回购
        "bond_sh_buy_back_em": svc.col_sh_buy_back,
        "bond_sz_buy_back_em": svc.col_sz_buy_back,
        "bond_buy_back_hist_em": svc.col_buybacks_hist,
        # 22-25 集思录数据
        "bond_cb_jsl": svc.col_cov_jsl,
        "bond_cb_redeem_jsl": svc.col_cov_redeem_jsl,
        "bond_cb_index_jsl": svc.col_cov_index_jsl,
        "bond_cb_adj_logs_jsl": svc.col_cov_adj_jsl,
        # 26-27 收益率曲线
        "bond_china_close_return": svc.col_yield_curve_hist,
        "bond_zh_us_rate": svc.col_cn_us_yield,
        # 28-32 债券发行
        "bond_treasure_issue_cninfo": svc.col_treasury_issue,
        "bond_local_government_issue_cninfo": svc.col_local_issue,
        "bond_corporate_issue_cninfo": svc.col_corporate_issue,
        "bond_cov_issue_cninfo": svc.col_cov_issue,
        "bond_cov_stock_issue_cninfo": svc.col_cov_convert,
        # 33-34 中债指数
        "bond_new_composite_index_cbond": svc.col_zh_bond_new_index,
        "bond_composite_index_cbond": svc.col_zh_bond_index,
        # 其他辅助集合（保留原有的映射）
        "bond_basic_info": svc.col_basic,
        "bond_daily": svc.col_daily,
        "yield_curve_daily": svc.col_curve,
        "bond_spot_quotes": svc.col_spot,
        "bond_minute_quotes": svc.col_minute,
        "bond_cb_profiles": svc.col_cb_profiles,
        "bond_cb_valuation_daily": svc.col_cb_valuation,
        "bond_cb_comparison": svc.col_cb_comparison,
        "bond_cb_adjustments": svc.col_cb_adjustments,
        "bond_cb_redeems": svc.col_cb_redeems,
        "bond_issues": svc.col_issues,
        "bond_buybacks": svc.col_buybacks,
        "bond_indices_daily": svc.col_indices,
        "us_yield_daily": svc.col_us_yield,
        "bond_spot_quote_detail": svc.col_spot_quote_detail,
        "bond_spot_deals": svc.col_spot_deals,
        "bond_deal_summary": svc.col_deal_summary,
        "bond_cash_summary": svc.col_cash_summary,
        "bond_nafmii_debts": svc.col_nafmii,
        "bond_cov_list": svc.col_cov_list,
        "bond_cb_list_jsl": svc.col_cb_list_jsl,
        "bond_cb_summary": svc.col_cb_summary,
        "bond_events": svc.col_events,
        "yield_curve_map": svc.col_curve_map,
    }
    
    collection = collection_map.get(collection_name)
    if collection is None:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    
    try:
        logger.info(f"📊 [集合统计] 开始获取集合 {collection_name} 的统计信息")
        
        # 总记录数
        try:
            total_count = await collection.count_documents({})
            logger.info(f"📊 [集合统计] 集合 {collection_name} 总记录数: {total_count}")
        except Exception as count_err:
            logger.error(f"❌ [集合统计] 获取总记录数失败: {count_err}", exc_info=True)
            total_count = 0
        
        # 获取最早和最晚的日期（如果有date或datetime字段）
        stats = {
            "total_count": total_count,
            "collection_name": collection_name,
        }
        
        # 尝试获取日期范围
        date_fields = ["date", "datetime", "timestamp", "更新日期", "发行日期", "上市日期"]
        for date_field in date_fields:
            try:
                # 查找有该字段的文档
                first_doc = await collection.find_one({date_field: {"$exists": True}}, sort=[(date_field, 1)])
                last_doc = await collection.find_one({date_field: {"$exists": True}}, sort=[(date_field, -1)])
                
                if first_doc is not None and last_doc is not None:
                    first_date = first_doc.get(date_field)
                    last_date = last_doc.get(date_field)
                    if first_date:
                        stats["earliest_date"] = str(first_date)[:10]
                    if last_date:
                        stats["latest_date"] = str(last_date)[:10]
                    stats["date_field"] = date_field
                    logger.info(f"📊 [集合统计] 找到日期字段 {date_field}: {stats.get('earliest_date')} - {stats.get('latest_date')}")
                    break
            except Exception as date_err:
                logger.debug(f"⚠️ [集合统计] 获取日期字段 {date_field} 失败: {date_err}")
                continue
        
        # 按类别统计（如果有category字段）
        try:
            pipeline = [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            category_stats = []
            async for doc in collection.aggregate(pipeline):
                category_id = doc.get("_id")
                count = doc.get("count", 0)
                category_stats.append({
                    "category": str(category_id) if category_id is not None else "未知",
                    "count": int(count)
                })
            if len(category_stats) > 0:
                stats["category_stats"] = category_stats
                logger.info(f"📊 [集合统计] 找到 {len(category_stats)} 个类别")
        except Exception as cat_err:
            logger.debug(f"⚠️ [集合统计] 获取类别统计失败: {cat_err}")
            pass
        
        # 按交易所统计（如果有exchange字段）
        try:
            pipeline = [
                {"$group": {"_id": "$exchange", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
            ]
            exchange_stats = []
            async for doc in collection.aggregate(pipeline):
                exchange_id = doc.get("_id")
                count = doc.get("count", 0)
                exchange_stats.append({
                    "exchange": str(exchange_id) if exchange_id is not None else "未知",
                    "count": int(count)
                })
            if len(exchange_stats) > 0:
                stats["exchange_stats"] = exchange_stats
                logger.info(f"📊 [集合统计] 找到 {len(exchange_stats)} 个交易所")
        except Exception as exch_err:
            logger.debug(f"⚠️ [集合统计] 获取交易所统计失败: {exch_err}")
            pass

        # bond_info_cm 专用统计：按“债券类型”和“最新债项评级”统计
        if collection_name == "bond_info_cm":
            # 债券类型分布
            try:
                pipeline = [
                    {
                        "$match": {
                            "$and": [
                                {"$or": [{"endpoint": "bond_info_cm"}, {"endpoint": {"$exists": False}}]},
                                {"债券类型": {"$exists": True, "$ne": ""}},
                            ]
                        }
                    },
                    {"$group": {"_id": "$债券类型", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                ]
                bond_type_stats: List[Dict[str, Any]] = []
                async for doc in collection.aggregate(pipeline):
                    type_id = doc.get("_id")
                    count = int(doc.get("count", 0))
                    bond_type_stats.append(
                        {"type": str(type_id) if type_id is not None else "未知", "count": count}
                    )
                if bond_type_stats:
                    stats["bond_type_stats"] = bond_type_stats
                    logger.info(f"📊 [集合统计] bond_info_cm 债券类型统计项数: {len(bond_type_stats)}")
            except Exception as type_err:
                logger.debug(f"⚠️ [集合统计] 获取债券类型统计失败: {type_err}")

            # 最新债项评级分布
            try:
                pipeline = [
                    {
                        "$match": {
                            "$and": [
                                {"$or": [{"endpoint": "bond_info_cm"}, {"endpoint": {"$exists": False}}]},
                                {"最新债项评级": {"$exists": True, "$ne": ""}},
                            ]
                        }
                    },
                    {"$group": {"_id": "$最新债项评级", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                ]
                grade_stats: List[Dict[str, Any]] = []
                async for doc in collection.aggregate(pipeline):
                    grade_id = doc.get("_id")
                    count = int(doc.get("count", 0))
                    grade_stats.append(
                        {"grade": str(grade_id) if grade_id is not None else "未知", "count": count}
                    )
                if grade_stats:
                    stats["grade_stats"] = grade_stats
                    logger.info(f"📊 [集合统计] bond_info_cm 最新债项评级统计项数: {len(grade_stats)}")
            except Exception as grade_err:
                logger.debug(f"⚠️ [集合统计] 获取债项评级统计失败: {grade_err}")

        logger.info(f"✅ [集合统计] 集合 {collection_name} 统计信息获取成功")
        return {"success": True, "data": stats}
    except HTTPException:
        # HTTPException应该直接抛出
        raise
    except Exception as e:
        logger.error(f"❌ [集合统计] 获取集合 {collection_name} 统计信息失败: {e}", exc_info=True)
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"❌ [集合统计] 错误堆栈: {error_trace}")
        raise HTTPException(
            status_code=500,
            detail=f"获取集合统计信息失败: {str(e)}"
        )


@router.get("/collections/bond_info_cm/issuance/yearly")
async def get_bond_info_cm_yearly_issuance(
    current_user: dict = Depends(get_current_user),
):
    """统计 bond_info_cm 集合按年份的债券发行数量"""
    db = get_mongo_db()
    svc = BondDataService(db)

    pipeline = [
        {"$match": {"endpoint": "bond_info_cm", "发行日期": {"$exists": True, "$ne": ""}}},
        {"$addFields": {"year": {"$substr": ["$发行日期", 0, 4]}}},
        {"$match": {"year": {"$regex": "^[0-9]{4}$"}}},
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]

    try:
        results: List[Dict[str, Any]] = []
        async for doc in svc.col_info_cm.aggregate(pipeline):
            year = str(doc.get("_id", ""))
            count = int(doc.get("count", 0))
            results.append({"year": year, "count": count})

        return {
            "success": True,
            "data": {
                "items": results,
                "total_years": len(results)
            }
        }
    except Exception as e:
        logger.error(f"❌ [bond_info_cm] 获取年度发行统计失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取年度发行统计失败: {str(e)}"
        )




# 债券分析相关模型
class BondAnalysisRequest(BaseModel):
    bond_code: str
    parameters: Optional[Dict[str, Any]] = {}


@router.post("/analysis")
async def start_bond_analysis(
    request: BondAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    """提交债券分析任务"""
    try:
        logger.info(f"🎯 收到债券分析请求: {request.bond_code}")
        
        # 验证债券代码格式
        bond_code = request.bond_code.strip()
        import re
        if not re.match(r'^\d{6}\.(SH|SZ|IB)$', bond_code, re.IGNORECASE):
            raise HTTPException(status_code=400, detail="债券代码格式不正确，应为：代码.交易所（如：110062.SH）")
        
        # 创建任务ID
        task_id = str(uuid.uuid4())
        
        # 导入分析服务
        from app.services.bond_analysis_service import get_bond_analysis_service
        service = get_bond_analysis_service()
        
        # 创建任务记录
        result = await service.create_analysis_task(
            user_id=current_user["id"],
            task_id=task_id,
            request=request
        )
        
        # 在后台执行分析任务
        async def run_analysis_task():
            try:
                logger.info(f"🚀 [BackgroundTask] 开始执行债券分析任务: {task_id}")
                await service.execute_analysis_background(task_id, current_user["id"], request)
                logger.info(f"✅ [BackgroundTask] 债券分析任务完成: {task_id}")
            except Exception as e:
                logger.error(f"❌ [BackgroundTask] 债券分析任务失败: {task_id}, 错误: {e}", exc_info=True)
        
        background_tasks.add_task(run_analysis_task)
        
        return {
            "success": True,
            "data": {"task_id": task_id},
            "message": "分析任务已在后台启动"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 提交债券分析任务失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{task_id}/status")
async def get_bond_analysis_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取债券分析任务状态"""
    try:
        from app.services.bond_analysis_service import get_bond_analysis_service
        service = get_bond_analysis_service()
        
        status = await service.get_task_status(task_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        return {
            "success": True,
            "data": status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 获取债券分析任务状态失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{task_id}/result")
async def get_bond_analysis_result(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取债券分析结果"""
    try:
        from app.services.bond_analysis_service import get_bond_analysis_service
        service = get_bond_analysis_service()
        
        result = await service.get_task_result(task_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="分析结果不存在")
        
        return {
            "success": True,
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 获取债券分析结果失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collections/{collection_name}/refresh")
async def refresh_collection_data(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    """从AKShare更新指定集合的数据（异步执行，支持进度查询）
    
    请求体参数（JSON）：
    - update_type: 'batch' 或 'single'，默认 'single'
    - concurrency: 并发数（批量更新时）
    - 其他参数根据集合不同而不同，参考 /collections/{collection_name}/update-config
    
    示例请求体：
    ```json
    {
        "update_type": "batch",
        "concurrency": 3,
        "year": "2024"
    }
    ```
    """
    try:
        logger.info(f"🔄 创建集合更新任务: {collection_name}, params={params}")
        
        db = get_mongo_db()
        task_manager = get_task_manager()
        
        # 使用新的 BondRefreshService
        from app.services.bond_refresh_service import BondRefreshService
        refresh_service = BondRefreshService(db)
        
        # 创建任务
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"更新集合: {collection_name}"
        )
        
        # 在后台异步执行刷新任务
        async def do_refresh():
            try:
                await refresh_service.refresh_collection(
                    collection_name, task_id, params
                )
            except Exception as e:
                logger.error(f"后台刷新任务失败: {e}", exc_info=True)
                # 确保任务状态被标记为失败
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)
        
        background_tasks.add_task(do_refresh)
        
        # 立即返回任务ID，前端可以用此ID查询进度
        return {
            "success": True,
            "data": {
                "task_id": task_id,
                "message": f"任务已创建，请使用 task_id 查询进度"
            }
        }
    
    except Exception as e:
        error_msg = f"创建更新任务失败: {str(e)}"
        logger.error(f"❌ {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)


@router.get("/collections/refresh/task/{task_id}")
async def get_refresh_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """查询数据刷新任务的进度"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)
        
        if not task:
            raise HTTPException(status_code=404, detail=f"任务 {task_id} 不存在")
        
        return {"success": True, "data": task}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 查询任务状态失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/collections/{collection_name}/import")
async def import_collection_data(
    collection_name: str,
    file: UploadFile = File(..., description="CSV 或 Excel 文件"),
    current_user: dict = Depends(get_current_user),
):
    """从文件导入债券集合数据（目前仅支持 bond_info_cm）"""
    try:
        logger.info(f"📥 [集合导入] collection={collection_name}, filename={file.filename}")

        if collection_name != "bond_info_cm":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前仅支持 bond_info_cm 集合的文件导入",
            )

        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")

        svc = BondDataService(db)
        content = await file.read()
        filename = file.filename or ""

        result = await svc.import_bond_info_cm_from_file(content, filename)
        saved = int(result.get("saved") or 0)
        rows = int(result.get("rows") or 0)

        message = f"成功导入 {saved} 条记录" if rows > 0 else "文件中没有可导入的数据"

        return {
            "success": True,
            "data": {
                "collection_name": collection_name,
                "saved": saved,
                "rows": rows,
                "message": message,
            },
        }
    except HTTPException:
        raise
    except ValueError as ve:
        logger.warning(f"⚠️ [集合导入] 参数错误: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"❌ [集合导入] 导入集合 {collection_name} 失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导入数据失败: {str(e)}")


@router.post("/collections/{collection_name}/sync-remote")
async def sync_collection_from_remote(
    collection_name: str,
    remote_host: str = Query(..., description="远程 MongoDB 主机地址或 URI"),
    db_type: str = Query("mongodb", description="数据库类型，目前仅支持 mongodb"),
    batch_size: int = Query(5000, ge=100, le=100000, description="每批次同步数量"),
    remote_collection: Optional[str] = Query(None, description="远程集合名称，默认为本地集合名"),
    remote_username: Optional[str] = Query(None, description="远程数据库用户名"),
    remote_password: Optional[str] = Query(None, description="远程数据库密码"),
    remote_auth_source: Optional[str] = Query(None, description="远程认证库（authSource），默认为目标数据库名"),
    current_user: dict = Depends(get_current_user),
):
    """从远程数据库同步集合数据到本地（当前仅支持 bond_info_cm 及 MongoDB）。"""
    try:
        logger.info(
            f"📡 [集合远程同步] collection={collection_name}, remote_host={remote_host}, db_type={db_type}, batch_size={batch_size}"
        )

        if collection_name != "bond_info_cm":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前仅支持 bond_info_cm 集合的远程同步",
            )

        if not remote_host:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="远程主机地址不能为空")

        if (db_type or "mongodb").lower() != "mongodb":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前仅支持 MongoDB 远程同步")

        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")

        svc = BondDataService(db)
        result = await svc.sync_collection_from_remote_mongo(
            collection_name=collection_name,
            remote_host=remote_host,
            batch_size=batch_size,
            remote_collection=remote_collection,
            remote_username=remote_username,
            remote_password=remote_password,
            remote_auth_source=remote_auth_source,
        )

        synced = int(result.get("synced") or 0)
        remote_total = int(result.get("remote_total") or 0)

        message = f"成功从远程同步 {synced} 条记录（远程共 {remote_total} 条）"

        return {
            "success": True,
            "data": {
                "collection_name": collection_name,
                "synced": synced,
                "remote_total": remote_total,
                "batch_size": batch_size,
                "message": message,
            },
        }
    except HTTPException:
        raise
    except ValueError as ve:
        logger.warning(f"⚠️ [集合远程同步] 参数错误: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"❌ [集合远程同步] 同步集合 {collection_name} 失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"远程同步失败: {str(e)}")


@router.delete("/collections/{collection_name}/clear")
async def clear_collection_data(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空集合数据
    
    删除指定集合中的所有数据，此操作不可恢复
    """
    try:
        logger.info(f"⚠️  [清空集合] 收到清空请求: collection={collection_name}, user={current_user.get('username')}")
        
        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        # 检查集合是否存在
        if collection_name not in await db.list_collection_names():
            raise HTTPException(status_code=404, detail=f"集合 {collection_name} 不存在")
        
        # 清空集合数据
        collection = db[collection_name]
        result = await collection.delete_many({})
        deleted_count = result.deleted_count
        
        logger.info(f"✅ [清空集合] 成功清空 {collection_name}，删除了 {deleted_count} 条记录")
        
        return {
            "success": True,
            "data": {
                "collection_name": collection_name,
                "deleted_count": deleted_count,
                "message": f"成功清空集合 {collection_name}，删除了 {deleted_count} 条记录"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 清空集合失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 可转债专项功能 ====================

@router.get("/convertible/comparison")
async def get_convertible_comparison(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页数量"),
    q: Optional[str] = Query(None, description="搜索关键词（代码或名称）"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("asc", description="排序方向：asc/desc"),
    min_premium: Optional[float] = Query(None, description="最小转股溢价率"),
    max_premium: Optional[float] = Query(None, description="最大转股溢价率"),
    current_user: dict = Depends(get_current_user),
):
    """获取可转债比价表
    
    返回可转债的实时比价数据，包括转股价、转股价值、溢价率等核心指标
    支持关键词搜索、溢价率范围过滤、排序和分页
    """
    try:
        logger.info(f"🔍 [可转债比价] 收到请求: page={page}, page_size={page_size}, q={q}, "
                   f"premium_range=[{min_premium}, {max_premium}]")
        
        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        svc = BondDataService(db)
        
        # 查询数据（在数据库层过滤，性能更好）
        result = await svc.query_cov_comparison(
            q=q,
            sort_by=sort_by,
            sort_dir=sort_dir,
            page=page,
            page_size=page_size,
            min_premium=min_premium,
            max_premium=max_premium
        )
        
        logger.info(f"✅ [可转债比价] 返回 {len(result.get('items', []))}/{result.get('total', 0)} 条数据")
        
        return {
            "success": True,
            "data": {
                "total": result.get("total", 0),
                "page": page,
                "page_size": page_size,
                "items": result.get("items", [])
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债比价] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convertible/comparison/sync")
async def sync_convertible_comparison(
    current_user: dict = Depends(get_current_user),
):
    """同步可转债比价数据
    
    从AKShare获取最新的可转债比价表数据并保存到数据库
    """
    try:
        logger.info(f"🔄 [可转债比价同步] 开始同步数据")
        
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        
        provider = AKShareBondProvider()
        df = await provider.get_cov_comparison()
        
        if df is None or df.empty:
            logger.warning("⚠️ [可转债比价同步] 未获取到数据")
            raise HTTPException(status_code=404, detail="未获取到数据")
        
        logger.info(f"📡 [可转债比价同步] 获取到 {len(df)} 条数据")
        
        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        svc = BondDataService(db)
        saved = await svc.save_cov_comparison(df)
        
        logger.info(f"✅ [可转债比价同步] 成功保存 {saved} 条数据")
        
        return {
            "success": True,
            "data": {
                "saved": saved,
                "total": len(df),
                "message": f"成功同步 {saved} 条可转债比价数据"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债比价同步] 失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/convertible/{code}/value-analysis")
async def get_convertible_value_analysis(
    code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user),
):
    """获取可转债价值分析历史数据
    
    返回指定可转债的历史价值分析数据，包括纯债价值、转股价值、溢价率走势等
    """
    try:
        logger.info(f"🔍 [可转债价值分析] 查询 {code}")
        
        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        svc = BondDataService(db)
        
        # 查询数据库
        result = await svc.query_cov_value_analysis(
            code=code,
            start_date=start_date,
            end_date=end_date
        )
        
        # 如果数据库没有数据，尝试从AKShare获取
        if not result.get("data"):
            logger.info(f"📡 [可转债价值分析] 数据库无数据，从AKShare获取")
            
            from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
            provider = AKShareBondProvider()
            df = await provider.get_cov_value_analysis(code)
            
            if df is not None and not df.empty:
                # 保存到数据库
                saved = await svc.save_cov_value_analysis(code, df)
                logger.info(f"💾 [可转债价值分析] 保存 {saved} 条数据")
                
                # 重新查询
                result = await svc.query_cov_value_analysis(
                    code=code,
                    start_date=start_date,
                    end_date=end_date
                )
        
        logger.info(f"✅ [可转债价值分析] 返回 {len(result.get('data', []))} 条数据")
        
        return {
            "success": True,
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债价值分析] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/convertible/{code}/value-analysis/sync")
async def sync_convertible_value_analysis(
    code: str,
    current_user: dict = Depends(get_current_user),
):
    """同步指定可转债的价值分析数据"""
    try:
        logger.info(f"🔄 [价值分析同步] 同步 {code}")
        
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        
        provider = AKShareBondProvider()
        df = await provider.get_cov_value_analysis(code)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="未获取到数据")
        
        db = get_mongo_db()
        if db is None:
            raise HTTPException(status_code=500, detail="数据库连接失败")
        
        svc = BondDataService(db)
        saved = await svc.save_cov_value_analysis(code, df)
        
        logger.info(f"✅ [价值分析同步] 保存 {saved} 条数据")
        
        return {
            "success": True,
            "data": {
                "saved": saved,
                "total": len(df),
                "message": f"成功同步 {saved} 条价值分析数据"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [价值分析同步] 失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/spot-deals")
async def get_spot_deals(
    current_user: dict = Depends(get_current_user),
):
    """获取现券市场成交行情
    
    返回银行间现券市场的实时成交数据
    """
    try:
        logger.info(f"🔍 [现券成交] 查询成交行情")
        
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        
        provider = AKShareBondProvider()
        df = await provider.get_spot_deal()
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="未获取到数据")
        
        # 转换为字典列表
        items = df.to_dict(orient="records")
        
        # 清理NaN值
        import math
        for item in items:
            for key, value in list(item.items()):
                if isinstance(value, float) and math.isnan(value):
                    item[key] = None
        
        logger.info(f"✅ [现券成交] 返回 {len(items)} 条数据")
        
        return {
            "success": True,
            "data": {
                "total": len(items),
                "items": items
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [现券成交] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/spot-quotes")
async def get_spot_quotes(
    current_user: dict = Depends(get_current_user),
):
    """获取现券市场做市报价
    
    返回银行间现券市场的做市商报价数据
    """
    try:
        logger.info(f"🔍 [现券报价] 查询做市报价")
        
        from tradingagents.dataflows.providers.china.bonds import AKShareBondProvider
        
        provider = AKShareBondProvider()
        df = await provider.get_spot_quote()
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="未获取到数据")
        
        # 转换为字典列表
        items = df.to_dict(orient="records")
        
        # 清理NaN值
        import math
        for item in items:
            for key, value in list(item.items()):
                if isinstance(value, float) and math.isnan(value):
                    item[key] = None
        
        logger.info(f"✅ [现券报价] 返回 {len(items)} 条数据")
        
        return {
            "success": True,
            "data": {
                "total": len(items),
                "items": items
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [现券报价] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/reset-init")
async def reset_initialization(
    current_user: dict = Depends(get_current_user),
):
    """管理端点：重置债券数据初始化状态
    
    当数据初始化出现问题时，可以通过此端点手动重置初始化状态，
    允许系统重新从AKShare获取数据。
    
    注意：仅管理员应该使用此端点
    """
    global _init_completed, _init_timestamp, _init_in_progress
    
    try:
        logger.warning(f"⚠️ [管理] 用户 {current_user.get('username')} 请求重置初始化状态")
        
        old_status = {
            "completed": _init_completed,
            "timestamp": _init_timestamp.isoformat() if _init_timestamp else None,
            "in_progress": _init_in_progress
        }
        
        # 重置状态
        _init_completed = False
        _init_timestamp = None
        # 不重置 _init_in_progress，避免干扰正在进行的初始化
        
        logger.info(f"✅ [管理] 初始化状态已重置")
        
        return {
            "success": True,
            "message": "初始化状态已重置，下次查询将重新获取数据",
            "old_status": old_status,
            "new_status": {
                "completed": _init_completed,
                "timestamp": None,
                "in_progress": _init_in_progress
            }
        }
    
    except Exception as e:
        logger.error(f"❌ [管理] 重置初始化状态失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 债券基础信息批量更新API ====================

@router.post("/basic-info/batch-update")
async def start_bond_basic_batch_update(
    batch_size: int = Query(1000, ge=100, le=5000, description="每批处理的数量"),
    concurrent_threads: int = Query(3, ge=1, le=10, description="并发线程数"),
    save_interval: int = Query(1000, ge=500, le=2000, description="保存间隔"),
    current_user: dict = Depends(get_current_user),
):
    """
    启动债券基础信息批量更新
    
    从bond_info_cm表查询债券简称，然后获取详细信息更新到bond_info_detail_cm中。
    采用多线程批量更新，每获取指定数量的数据保存到集合一次。
    """
    try:
        from app.services.bond_basic_info_service import BondBasicInfoService
        
        db = get_mongo_db()
        service = BondBasicInfoService(db)
        
        logger.info(f"🚀 [批量更新API] 用户 {current_user.get('username')} 启动债券基础信息批量更新")
        logger.info(f"📊 [批量更新API] 参数: batch_size={batch_size}, threads={concurrent_threads}, save_interval={save_interval}")
        
        # 执行批量更新
        result = await service.batch_update_from_bond_info_cm(
            batch_size=batch_size,
            concurrent_threads=concurrent_threads,
            save_interval=save_interval
        )
        
        if result.get("success"):
            logger.info(f"✅ [批量更新API] 批量更新完成: {result.get('message')}")
            return {"success": True, "data": result}
        else:
            logger.error(f"❌ [批量更新API] 批量更新失败: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error"))
            
    except Exception as e:
        logger.error(f"❌ [批量更新API] 执行失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/basic-info/incremental-update")
async def start_bond_basic_incremental_update(
    current_user: dict = Depends(get_current_user),
):
    """
    启动债券基础信息增量更新
    
    从bond_info_cm集合中查询债券简称，然后从bond_info_detail_cm集合中获取已有的债券代码，
    找出缺失的债券基础信息并更新到集合中。
    """
    try:
        from app.services.bond_basic_info_service import BondBasicInfoService
        
        db = get_mongo_db()
        service = BondBasicInfoService(db)
        
        logger.info(f"🔍 [增量更新API] 用户 {current_user.get('username')} 启动债券基础信息增量更新")
        
        # 执行增量更新
        result = await service.incremental_update_missing_info()
        
        if result.get("success"):
            logger.info(f"✅ [增量更新API] 增量更新完成: {result.get('message')}")
            return {"success": True, "data": result}
        else:
            logger.error(f"❌ [增量更新API] 增量更新失败: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error"))
            
    except Exception as e:
        logger.error(f"❌ [增量更新API] 执行失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/basic-info/update-statistics")
async def get_bond_basic_update_statistics(
    current_user: dict = Depends(get_current_user),
):
    """
    获取债券基础信息更新统计
    
    返回bond_info_cm和bond_info_detail_cm的记录数量、覆盖率等统计信息。
    """
    try:
        from app.services.bond_basic_info_service import BondBasicInfoService
        
        db = get_mongo_db()
        service = BondBasicInfoService(db)
        
        logger.debug(f"📊 [统计API] 用户 {current_user.get('username')} 查询债券基础信息更新统计")
        
        # 获取统计信息
        result = await service.get_update_statistics()
        
        if result.get("success"):
            return {"success": True, "data": result}
        else:
            logger.error(f"❌ [统计API] 获取统计失败: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error"))
            
    except Exception as e:
        logger.error(f"❌ [统计API] 执行失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 03号需求：沪深债券实时行情 ====================

@router.get("/zh-hs-spot")
async def get_bond_zh_hs_spot(
    q: Optional[str] = Query(None, description="关键词过滤（代码或名称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("涨跌幅", description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取沪深债券实时行情数据
    
    - 支持关键词搜索
    - 支持分页
    - 支持按涨跌幅、成交量、成交额等排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [沪深债券实时行情] 查询请求: q={q}, page={page}, sort_by={sort_by}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_spot(
            q=q,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [沪深债券实时行情] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [沪深债券实时行情] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-spot/refresh")
async def refresh_bond_zh_hs_spot(
    start_page: int = Query(1, ge=1, description="开始页码"),
    end_page: int = Query(5, ge=1, le=50, description="结束页码"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新沪深债券实时行情数据
    
    - 从AKShare获取指定页面范围的实时行情
    - 每页80条数据
    - 使用代码作为唯一标识进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [沪深债券实时行情] 开始刷新: page {start_page}-{end_page}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_spot(start_page=str(start_page), end_page=str(end_page))
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [沪深债券实时行情] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            # 转换为字典列表
            data = df.to_dict('records')
            logger.info(f"📡 [沪深债券实时行情] 从AKShare获取{len(data)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_spot(data)
            
            logger.info(f"✅ [沪深债券实时行情] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(data),
                    "saved": saved_count,
                    "start_page": start_page,
                    "end_page": end_page
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [沪深债券实时行情] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [沪深债券实时行情] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 04号需求：沪深债券历史行情 ====================

@router.get("/zh-hs-daily/{symbol}")
async def get_bond_zh_hs_daily(
    symbol: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取指定债券的历史行情数据
    
    - 按日期倒序返回
    - 支持日期范围筛选
    - 支持分页
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [沪深债券历史行情] 查询 {symbol}: {start_date} ~ {end_date}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_daily(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [沪深债券历史行情] {symbol} 查询成功: total={result['total']}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [沪深债券历史行情] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-daily/{symbol}/refresh")
async def refresh_bond_zh_hs_daily(
    symbol: str,
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定债券的历史行情数据
    
    - 从AKShare获取该债券的全部历史数据
    - 使用symbol+date作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [沪深债券历史行情] 开始刷新 {symbol}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_daily(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [沪深债券历史行情] {symbol} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [沪深债券历史行情] {symbol} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_daily(symbol, df)
            
            logger.info(f"✅ [沪深债券历史行情] {symbol} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [沪深债券历史行情] {symbol} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [沪深债券历史行情] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-daily/batch-refresh")
async def batch_refresh_bond_zh_hs_daily(
    symbols: list[str] = Query(..., description="债券代码列表"),
    current_user: dict = Depends(get_current_user),
):
    """
    批量刷新多个债券的历史行情数据
    
    - 依次获取每个债券的历史数据
    - 返回成功和失败的统计
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [沪深债券历史行情] 批量刷新 {len(symbols)} 个债券")
        
        results = {"success": [], "failed": []}
        
        import akshare as ak
        import asyncio
        
        for symbol in symbols:
            try:
                # 获取数据
                df = ak.bond_zh_hs_daily(symbol=symbol)
                
                if df is None or df.empty:
                    results["failed"].append({"symbol": symbol, "error": "无数据"})
                    continue
                
                # 保存数据
                saved_count = await svc.save_bond_zh_hs_daily(symbol, df)
                results["success"].append({"symbol": symbol, "count": saved_count})
                
                # 避免API限流
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"❌ [批量刷新] {symbol} 失败: {e}")
                results["failed"].append({"symbol": symbol, "error": str(e)})
        
        logger.info(f"✅ [沪深债券历史行情] 批量刷新完成: 成功{len(results['success'])}, 失败{len(results['failed'])}")
        return {"success": True, "data": results}
        
    except Exception as e:
        logger.error(f"❌ [沪深债券历史行情] 批量刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 05号需求：可转债实时行情-沪深 ====================

@router.get("/zh-hs-cov-spot")
async def get_bond_zh_hs_cov_spot(
    q: Optional[str] = Query(None, description="关键词过滤（代码或名称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("changepercent", description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债实时行情数据
    
    - 支持关键词搜索（代码、名称、symbol）
    - 支持分页
    - 支持按涨跌幅、成交额等排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债实时行情] 查询请求: q={q}, page={page}, sort_by={sort_by}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_cov_spot(
            q=q,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [可转债实时行情] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债实时行情] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-cov-spot/refresh")
async def refresh_bond_zh_hs_cov_spot(
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债实时行情数据
    
    - 从AKShare获取所有可转债的实时行情
    - 使用code作为唯一标识进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债实时行情] 开始刷新")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_cov_spot()
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债实时行情] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            # 转换为字典列表
            data = df.to_dict('records')
            logger.info(f"📡 [可转债实时行情] 从AKShare获取{len(data)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_cov_spot(data)
            
            logger.info(f"✅ [可转债实时行情] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(data),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债实时行情] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债实时行情] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 06号需求：可转债历史行情-日频 ====================

@router.get("/zh-hs-cov-daily/{symbol}")
async def get_bond_zh_hs_cov_daily(
    symbol: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取指定可转债的历史行情数据
    
    - 按日期倒序返回
    - 支持日期范围筛选
    - 支持分页
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债历史行情] 查询 {symbol}: {start_date} ~ {end_date}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_cov_daily(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [可转债历史行情] {symbol} 查询成功: total={result['total']}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债历史行情] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-cov-daily/{symbol}/refresh")
async def refresh_bond_zh_hs_cov_daily(
    symbol: str,
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定可转债的历史行情数据
    
    - 从AKShare获取该可转债的全部历史数据
    - 使用symbol+date作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债历史行情] 开始刷新 {symbol}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_cov_daily(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债历史行情] {symbol} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [可转债历史行情] {symbol} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_cov_daily(symbol, df)
            
            logger.info(f"✅ [可转债历史行情] {symbol} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债历史行情] {symbol} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债历史行情] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-cov-daily/batch-refresh")
async def batch_refresh_bond_zh_hs_cov_daily(
    symbols: list[str] = Query(..., description="可转债代码列表"),
    current_user: dict = Depends(get_current_user),
):
    """
    批量刷新多个可转债的历史行情数据
    
    - 依次获取每个可转债的历史数据
    - 返回成功和失败的统计
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债历史行情] 批量刷新 {len(symbols)} 个可转债")
        
        results = {"success": [], "failed": []}
        
        import akshare as ak
        import asyncio
        
        for symbol in symbols:
            try:
                # 获取数据
                df = ak.bond_zh_hs_cov_daily(symbol=symbol)
                
                if df is None or df.empty:
                    results["failed"].append({"symbol": symbol, "error": "无数据"})
                    continue
                
                # 保存数据
                saved_count = await svc.save_bond_zh_hs_cov_daily(symbol, df)
                results["success"].append({"symbol": symbol, "count": saved_count})
                
                # 避免API限流
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"❌ [批量刷新] {symbol} 失败: {e}")
                results["failed"].append({"symbol": symbol, "error": str(e)})
        
        logger.info(f"✅ [可转债历史行情] 批量刷新完成: 成功{len(results['success'])}, 失败{len(results['failed'])}")
        return {"success": True, "data": results}
        
    except Exception as e:
        logger.error(f"❌ [可转债历史行情] 批量刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 07号需求：可转债数据一览表-东财 ====================

@router.get("/zh-cov")
async def get_bond_zh_cov(
    q: Optional[str] = Query(None, description="关键词过滤（代码或名称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("转股溢价率", description="排序字段"),
    sort_dir: str = Query("asc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债数据一览表（东财）
    
    - 支持关键词搜索（债券代码、债券简称、正股代码、正股简称）
    - 支持分页
    - 支持按转股溢价率、发行规模等排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债一览表] 查询请求: q={q}, page={page}, sort_by={sort_by}")
        
        # 查询数据
        result = await svc.query_bond_zh_cov(
            q=q,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [可转债一览表] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债一览表] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-cov/refresh")
async def refresh_bond_zh_cov(
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债数据一览表
    
    - 从AKShare获取东财的所有可转债一览数据
    - 使用债券代码作为唯一标识进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债一览表] 开始刷新")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_cov()
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债一览表] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            # 转换为字典列表
            data = df.to_dict('records')
            logger.info(f"📡 [可转债一览表] 从AKShare获取{len(data)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_cov(data)
            
            logger.info(f"✅ [可转债一览表] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(data),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债一览表] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债一览表] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 08号需求：债券现券市场概览-上交所 ====================

@router.get("/cash-summary-sse")
async def get_bond_cash_summary_sse(
    date: Optional[str] = Query(None, description="数据日期 YYYY-MM-DD"),
    bond_type: Optional[str] = Query(None, description="债券类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取债券现券市场概览数据（上交所）
    
    - 按日期查询市场概览
    - 支持债券类型筛选
    - 支持分页
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [现券市场概览] 查询请求: date={date}, bond_type={bond_type}")
        
        # 查询数据
        result = await svc.query_bond_cash_summary_sse(
            date=date,
            bond_type=bond_type,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [现券市场概览] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [现券市场概览] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cash-summary-sse/refresh")
async def refresh_bond_cash_summary_sse(
    date: str = Query(..., description="数据日期，格式：20210111"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定日期的债券现券市场概览数据
    
    - 从AKShare获取指定日期的市场概览数据
    - 使用债券类型+日期作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [现券市场概览] 开始刷新 {date}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_cash_summary_sse(date=date)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [现券市场概览] {date} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [现券市场概览] {date} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_cash_summary_sse(date, df)
            
            logger.info(f"✅ [现券市场概览] {date} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "date": date,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [现券市场概览] {date} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [现券市场概览] {date} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cash-summary-sse/batch-refresh")
async def batch_refresh_bond_cash_summary_sse(
    start_date: str = Query(..., description="开始日期，格式：20210101"),
    end_date: str = Query(..., description="结束日期，格式：20210131"),
    current_user: dict = Depends(get_current_user),
):
    """
    批量刷新日期范围内的债券现券市场概览数据
    
    - 依次获取日期范围内每个交易日的数据
    - 返回成功和失败的统计
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [现券市场概览] 批量刷新 {start_date} ~ {end_date}")
        
        results = {"success": [], "failed": []}
        
        import akshare as ak
        import asyncio
        from datetime import datetime, timedelta
        
        # 生成日期列表
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y%m%d"))
            current += timedelta(days=1)
        
        for date in date_list:
            try:
                # 获取数据
                df = ak.bond_cash_summary_sse(date=date)
                
                if df is None or df.empty:
                    results["failed"].append({"date": date, "error": "无数据"})
                    continue
                
                # 保存数据
                saved_count = await svc.save_bond_cash_summary_sse(date, df)
                results["success"].append({"date": date, "count": saved_count})
                
                # 避免API限流
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"❌ [批量刷新] {date} 失败: {e}")
                results["failed"].append({"date": date, "error": str(e)})
        
        logger.info(f"✅ [现券市场概览] 批量刷新完成: 成功{len(results['success'])}, 失败{len(results['failed'])}")
        return {"success": True, "data": results}
        
    except Exception as e:
        logger.error(f"❌ [现券市场概览] 批量刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 09号需求：债券成交概览-上交所 ====================

@router.get("/deal-summary-sse")
async def get_bond_deal_summary_sse(
    date: Optional[str] = Query(None, description="数据日期 YYYY-MM-DD"),
    bond_type: Optional[str] = Query(None, description="债券类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取债券成交概览数据（上交所）
    
    - 按日期查询成交概览
    - 支持债券类型筛选
    - 包含当日成交和当年累计成交数据
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [债券成交概览] 查询请求: date={date}, bond_type={bond_type}")
        
        # 查询数据
        result = await svc.query_bond_deal_summary_sse(
            date=date,
            bond_type=bond_type,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [债券成交概览] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [债券成交概览] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deal-summary-sse/refresh")
async def refresh_bond_deal_summary_sse(
    date: str = Query(..., description="数据日期，格式：20210104"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定日期的债券成交概览数据
    
    - 从AKShare获取指定日期的成交概览数据
    - 使用债券类型+日期作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [债券成交概览] 开始刷新 {date}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_deal_summary_sse(date=date)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [债券成交概览] {date} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [债券成交概览] {date} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_deal_summary_sse(date, df)
            
            logger.info(f"✅ [债券成交概览] {date} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "date": date,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [债券成交概览] {date} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [债券成交概览] {date} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/deal-summary-sse/batch-refresh")
async def batch_refresh_bond_deal_summary_sse(
    start_date: str = Query(..., description="开始日期，格式：20210101"),
    end_date: str = Query(..., description="结束日期，格式：20210131"),
    current_user: dict = Depends(get_current_user),
):
    """
    批量刷新日期范围内的债券成交概览数据
    
    - 依次获取日期范围内每个交易日的数据
    - 返回成功和失败的统计
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [债券成交概览] 批量刷新 {start_date} ~ {end_date}")
        
        results = {"success": [], "failed": []}
        
        import akshare as ak
        import asyncio
        from datetime import datetime, timedelta
        
        # 生成日期列表
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y%m%d"))
            current += timedelta(days=1)
        
        for date in date_list:
            try:
                # 获取数据
                df = ak.bond_deal_summary_sse(date=date)
                
                if df is None or df.empty:
                    results["failed"].append({"date": date, "error": "无数据"})
                    continue
                
                # 保存数据
                saved_count = await svc.save_bond_deal_summary_sse(date, df)
                results["success"].append({"date": date, "count": saved_count})
                
                # 避免API限流
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"❌ [批量刷新] {date} 失败: {e}")
                results["failed"].append({"date": date, "error": str(e)})
        
        logger.info(f"✅ [债券成交概览] 批量刷新完成: 成功{len(results['success'])}, 失败{len(results['failed'])}")
        return {"success": True, "data": results}
        
    except Exception as e:
        logger.error(f"❌ [债券成交概览] 批量刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 10号需求：银行间市场债券发行数据 ====================

@router.get("/debt-nafmii")
async def get_bond_debt_nafmii(
    q: Optional[str] = Query(None, description="关键词过滤（债券名称）"),
    bond_type: Optional[str] = Query(None, description="品种（SCP、MTN等）"),
    status: Optional[str] = Query(None, description="项目状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("更新日期", description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取银行间市场债券发行数据
    
    - 支持按债券名称搜索
    - 支持按品种筛选（SCP、MTN、CP等）
    - 支持按项目状态筛选
    - 支持分页和排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [银行间债券发行] 查询请求: q={q}, type={bond_type}, status={status}")
        
        # 查询数据
        result = await svc.query_bond_debt_nafmii(
            q=q,
            bond_type=bond_type,
            status=status,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [银行间债券发行] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [银行间债券发行] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debt-nafmii/refresh")
async def refresh_bond_debt_nafmii(
    page: int = Query(1, description="页码，每页50条数据"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新指定页的银行间市场债券发行数据
    
    - 从AKShare获取指定页的数据（每页50条）
    - 使用债券名称+注册通知书文号作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [银行间债券发行] 开始刷新第{page}页")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_debt_nafmii(page=str(page))
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [银行间债券发行] 第{page}页 AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [银行间债券发行] 第{page}页 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_debt_nafmii(df)
            
            logger.info(f"✅ [银行间债券发行] 第{page}页 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "page": page,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [银行间债券发行] 第{page}页 AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [银行间债券发行] 第{page}页 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debt-nafmii/batch-refresh")
async def batch_refresh_bond_debt_nafmii(
    start_page: int = Query(1, description="开始页码"),
    end_page: int = Query(10, description="结束页码"),
    current_user: dict = Depends(get_current_user),
):
    """
    批量刷新多页银行间市场债券发行数据
    
    - 依次获取页码范围内的数据
    - 每页50条数据
    - 返回成功和失败的统计
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [银行间债券发行] 批量刷新 第{start_page}-{end_page}页")
        
        results = {"success": [], "failed": []}
        
        import akshare as ak
        import asyncio
        
        for page in range(start_page, end_page + 1):
            try:
                # 获取数据
                df = ak.bond_debt_nafmii(page=str(page))
                
                if df is None or df.empty:
                    results["failed"].append({"page": page, "error": "无数据"})
                    continue
                
                # 保存数据
                saved_count = await svc.save_bond_debt_nafmii(df)
                results["success"].append({"page": page, "count": saved_count})
                
                # 避免API限流
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"❌ [批量刷新] 第{page}页 失败: {e}")
                results["failed"].append({"page": page, "error": str(e)})
        
        logger.info(f"✅ [银行间债券发行] 批量刷新完成: 成功{len(results['success'])}, 失败{len(results['failed'])}")
        return {"success": True, "data": results}
        
    except Exception as e:
        logger.error(f"❌ [银行间债券发行] 批量刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 11号需求：现券市场做市报价 ====================

@router.get("/spot-quote")
async def get_bond_spot_quote(
    q: Optional[str] = Query(None, description="关键词过滤（债券简称）"),
    organization: Optional[str] = Query(None, description="报价机构"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("更新时间", description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取现券市场做市报价数据
    
    - 支持按债券简称搜索
    - 支持按报价机构筛选
    - 包含买入净价、卖出净价、买卖价差等
    - 支持分页和排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [现券做市报价] 查询请求: q={q}, org={organization}")
        
        # 查询数据
        result = await svc.query_bond_spot_quote(
            q=q,
            organization=organization,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [现券做市报价] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [现券做市报价] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/spot-quote/refresh")
async def refresh_bond_spot_quote(
    current_user: dict = Depends(get_current_user),
):
    """
    刷新现券市场做市报价数据
    
    - 从AKShare获取所有做市报价数据
    - 使用报价机构+债券简称作为联合主键进行upsert
    - 自动计算买卖价差
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [现券做市报价] 开始刷新")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_spot_quote()
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [现券做市报价] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [现券做市报价] 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_spot_quote(df)
            
            logger.info(f"✅ [现券做市报价] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [现券做市报价] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [现券做市报价] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 12号需求：现券市场成交行情 ====================

@router.get("/spot-deal")
async def get_bond_spot_deal(
    q: Optional[str] = Query(None, description="关键词过滤（债券简称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("交易量", description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取现券市场成交行情数据
    
    - 支持按债券简称搜索
    - 包含成交净价、最新收益率、涨跌（BP）、加权收益率、交易量等
    - 支持按交易量、涨跌等排序
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [现券成交行情] 查询请求: q={q}")
        
        # 查询数据
        result = await svc.query_bond_spot_deal(
            q=q,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_dir=sort_dir
        )
        
        logger.info(f"✅ [现券成交行情] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [现券成交行情] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/spot-deal/refresh")
async def refresh_bond_spot_deal(
    current_user: dict = Depends(get_current_user),
):
    """
    刷新现券市场成交行情数据
    
    - 从AKShare获取所有成交行情数据
    - 使用债券简称作为唯一标识进行upsert
    - 包含实时成交净价、收益率、涨跌等信息
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [现券成交行情] 开始刷新")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_spot_deal()
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [现券成交行情] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [现券成交行情] 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_spot_deal(df)
            
            logger.info(f"✅ [现券成交行情] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [现券成交行情] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [现券成交行情] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 13号需求：可转债分时行情 ====================

@router.get("/zh-hs-cov-min/{symbol}")
async def get_bond_zh_hs_cov_min(
    symbol: str,
    period: Optional[str] = Query(None, description="周期：1/5/15/30/60分钟"),
    adjust: Optional[str] = Query(None, description="复权：''/qfq/hfq"),
    start_time: Optional[str] = Query(None, description="开始时间 YYYY-MM-DD HH:MM:SS"),
    end_time: Optional[str] = Query(None, description="结束时间 YYYY-MM-DD HH:MM:SS"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(1000, ge=1, le=5000, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债分时行情数据
    
    - 支持多周期查询（1/5/15/30/60分钟）
    - 支持复权选择（不复权/前复权/后复权）
    - 支持时间范围筛选
    - 按时间升序返回
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债分时] 查询请求: {symbol}, period={period}, adjust={adjust}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_cov_min(
            symbol=symbol,
            period=period,
            adjust=adjust,
            start_time=start_time,
            end_time=end_time,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [可转债分时] {symbol} 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债分时] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-cov-min/{symbol}/refresh")
async def refresh_bond_zh_hs_cov_min(
    symbol: str,
    period: str = Query("5", description="周期：1/5/15/30/60分钟"),
    adjust: str = Query("", description="复权：''/qfq/hfq"),
    start_date: str = Query("1979-09-01 09:32:00", description="开始日期时间"),
    end_date: str = Query("2222-01-01 09:32:00", description="结束日期时间"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债分时行情数据
    
    - 从AKShare获取指定可转债、指定周期、复权方式的分时数据
    - 使用债券代码+时间+周期+复权方式作为联合主键进行upsert
    - 注意：1分钟数据只返回近1个交易日且不复权
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债分时] 开始刷新 {symbol} {period}分钟 {adjust if adjust else '不复权'}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_cov_min(
                symbol=symbol,
                period=period,
                adjust=adjust,
                start_date=start_date,
                end_date=end_date
            )
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债分时] {symbol} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [可转债分时] {symbol} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_cov_min(symbol, period, adjust, df)
            
            logger.info(f"✅ [可转债分时] {symbol} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "period": period,
                    "adjust": adjust if adjust else "不复权",
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债分时] {symbol} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债分时] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 14号需求：可转债盘前分时 ====================

@router.get("/zh-hs-cov-pre-min/{symbol}")
async def get_bond_zh_hs_cov_pre_min(
    symbol: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(1000, ge=1, le=5000, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债盘前分时数据
    
    - 返回最近一个交易日的盘前分时数据
    - 按时间升序返回
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债盘前] 查询请求: {symbol}")
        
        # 查询数据
        result = await svc.query_bond_zh_hs_cov_pre_min(
            symbol=symbol,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [可转债盘前] {symbol} 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债盘前] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-hs-cov-pre-min/{symbol}/refresh")
async def refresh_bond_zh_hs_cov_pre_min(
    symbol: str,
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债盘前分时数据
    
    - 从AKShare获取指定可转债最近一个交易日的盘前分时数据
    - 使用债券代码+时间作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债盘前] 开始刷新 {symbol}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_hs_cov_pre_min(symbol=symbol)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债盘前] {symbol} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [可转债盘前] {symbol} 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_hs_cov_pre_min(symbol, df)
            
            logger.info(f"✅ [可转债盘前] {symbol} 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债盘前] {symbol} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债盘前] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 15号需求：可转债详情-东财 ====================

@router.get("/zh-cov-info")
async def get_bond_zh_cov_info(
    symbol: Optional[str] = Query(None, description="债券代码"),
    indicator: Optional[str] = Query(None, description="指标类型：基本信息/中签号/筹资用途/重要日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债详情数据
    
    - 支持4种指标类型查询：基本信息、中签号、筹资用途、重要日期
    - 详情数据以JSON格式返回
    - 可查询单只债券或批量查询
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债详情] 查询请求: symbol={symbol}, indicator={indicator}")
        
        # 查询数据
        result = await svc.query_bond_zh_cov_info(
            symbol=symbol,
            indicator=indicator,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [可转债详情] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债详情] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-cov-info/{symbol}/refresh")
async def refresh_bond_zh_cov_info(
    symbol: str,
    indicator: str = Query("基本信息", description="指标类型：基本信息/中签号/筹资用途/重要日期"),
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债详情数据
    
    - 从AKShare获取指定可转债的详情数据
    - 支持4种指标类型：基本信息、中签号、筹资用途、重要日期
    - 使用债券代码+指标类型作为联合主键进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债详情] 开始刷新 {symbol} {indicator}")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_cov_info(symbol=symbol, indicator=indicator)
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债详情] {symbol} {indicator} AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [可转债详情] {symbol} {indicator} 从AKShare获取数据，字段数: {len(df.columns)}")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_cov_info(symbol, indicator, df)
            
            logger.info(f"✅ [可转债详情] {symbol} {indicator} 刷新完成")
            return {
                "success": True,
                "data": {
                    "symbol": symbol,
                    "indicator": indicator,
                    "fields": len(df.columns),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债详情] {symbol} {indicator} AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债详情] {symbol} {indicator} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 16号需求：可转债详情-同花顺 ====================

@router.get("/zh-cov-info-ths")
async def get_bond_zh_cov_info_ths(
    q: Optional[str] = Query(None, description="关键词（债券代码或简称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    """
    获取可转债详情数据（同花顺）
    
    - 包含16个字段的完整可转债信息
    - 支持按债券代码或简称搜索
    - 全量数据
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔍 [可转债详情THS] 查询请求: q={q}")
        
        # 查询数据
        result = await svc.query_bond_zh_cov_info_ths(
            q=q,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"✅ [可转债详情THS] 查询成功: total={result['total']}, items={len(result['items'])}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [可转债详情THS] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/zh-cov-info-ths/refresh")
async def refresh_bond_zh_cov_info_ths(
    current_user: dict = Depends(get_current_user),
):
    """
    刷新可转债详情数据（同花顺）
    
    - 从AKShare获取所有可转债的详情数据
    - 使用债券代码作为唯一标识进行upsert
    """
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        
        logger.info(f"🔄 [可转债详情THS] 开始刷新")
        
        # 获取数据
        try:
            import akshare as ak
            df = ak.bond_zh_cov_info_ths()
            
            if df is None or df.empty:
                logger.warning(f"⚠️ [可转债详情THS] AKShare返回空数据")
                return {"success": False, "error": "未获取到数据"}
            
            logger.info(f"📡 [可转债详情THS] 从AKShare获取{len(df)}条数据")
            
            # 保存到数据库
            saved_count = await svc.save_bond_zh_cov_info_ths(df)
            
            logger.info(f"✅ [可转债详情THS] 刷新完成: 保存{saved_count}条")
            return {
                "success": True,
                "data": {
                    "fetched": len(df),
                    "saved": saved_count
                }
            }
            
        except Exception as ak_error:
            logger.error(f"❌ [可转债详情THS] AKShare获取失败: {ak_error}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"数据获取失败: {str(ak_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ [可转债详情THS] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 17号需求：可转债比价表 ====================

@router.get("/cov-comparison")
async def get_bond_cov_comparison(
    q: Optional[str] = Query(None, description="关键词（转债代码或名称）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query("双低值", description="排序字段"),
    sort_dir: str = Query("asc", description="排序方向：asc|desc"),
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        result = await svc.query_bond_cov_comparison(q=q, page=page, page_size=page_size, sort_by=sort_by, sort_dir=sort_dir)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"❌ [可转债比价表] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cov-comparison/refresh")
async def refresh_bond_cov_comparison(current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        import akshare as ak
        df = ak.bond_cov_comparison()
        if df is None or df.empty:
            return {"success": False, "error": "未获取到数据"}
        saved_count = await svc.save_bond_cov_comparison(df)
        return {"success": True, "data": {"fetched": len(df), "saved": saved_count}}
    except Exception as e:
        logger.error(f"❌ [可转债比价表] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 18号需求：可转债价值分析 ====================

@router.get("/zh-cov-value-analysis/{symbol}")
async def get_bond_zh_cov_value_analysis(
    symbol: str,
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    current_user: dict = Depends(get_current_user),
):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        result = await svc.query_bond_zh_cov_value_analysis(symbol, start_date, end_date, page, page_size)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"❌ [可转债价值分析] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/zh-cov-value-analysis/{symbol}/refresh")
async def refresh_bond_zh_cov_value_analysis(symbol: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        import akshare as ak
        df = ak.bond_zh_cov_value_analysis(symbol=symbol)
        if df is None or df.empty:
            return {"success": False, "error": "未获取到数据"}
        saved_count = await svc.save_bond_zh_cov_value_analysis(symbol, df)
        return {"success": True, "data": {"symbol": symbol, "fetched": len(df), "saved": saved_count}}
    except Exception as e:
        logger.error(f"❌ [可转债价值分析] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 19-20号需求：质押式回购 ====================

@router.get("/buy-back/{market}")
async def get_bond_buy_back(market: str, page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500), current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        result = await svc.query_bond_buy_back(market, page, page_size)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"❌ [质押式回购{market}] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/buy-back/{market}/refresh")
async def refresh_bond_buy_back(market: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        import akshare as ak
        df = ak.bond_sh_buy_back_em() if market == "sh" else ak.bond_sz_buy_back_em()
        if df is None or df.empty:
            return {"success": False, "error": "未获取到数据"}
        saved_count = await svc.save_bond_buy_back(df, market)
        return {"success": True, "data": {"market": market, "fetched": len(df), "saved": saved_count}}
    except Exception as e:
        logger.error(f"❌ [质押式回购{market}] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 21号需求：回购历史数据 ====================

@router.get("/repo-hist/{symbol}")
async def get_bond_repo_hist(symbol: str, page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500), current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        result = await svc.query_bond_repo_hist(symbol, page, page_size)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"❌ [回购历史] {symbol} 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/repo-hist/{symbol}/refresh")
async def refresh_bond_repo_hist(symbol: str, current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        import akshare as ak
        df = ak.bond_repo_zh_hist(symbol=symbol)
        if df is None or df.empty:
            return {"success": False, "error": "未获取到数据"}
        saved_count = await svc.save_bond_repo_hist(symbol, df)
        return {"success": True, "data": {"symbol": symbol, "fetched": len(df), "saved": saved_count}}
    except Exception as e:
        logger.error(f"❌ [回购历史] {symbol} 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 22号需求：可转债实时数据-集思录 ====================

@router.get("/cov-jsl")
async def get_bond_cov_jsl(q: Optional[str] = Query(None), page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500), current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        result = await svc.query_bond_cov_jsl(q, page, page_size)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"❌ [可转债JSL] 查询失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cov-jsl/refresh")
async def refresh_bond_cov_jsl(current_user: dict = Depends(get_current_user)):
    try:
        db = get_mongo_db()
        svc = BondDataService(db)
        import akshare as ak
        df = ak.bond_cov_jsl()
        if df is None or df.empty:
            return {"success": False, "error": "未获取到数据"}
        saved_count = await svc.save_bond_cov_jsl(df)
        return {"success": True, "data": {"fetched": len(df), "saved": saved_count}}
    except Exception as e:
        logger.error(f"❌ [可转债JSL] 刷新失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 23-34号需求：使用通用方法 ====================

# 23号需求：可转债强赎-集思录
@router.get("/cov-redeem-jsl")
async def get_bond_cov_redeem_jsl(page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500), current_user: dict = Depends(get_current_user)):
    db, svc = get_mongo_db(), BondDataService(get_mongo_db())
    result = await svc.query_generic_bond_data(svc.col_cov_redeem_jsl, {}, "可转债强赎JSL", page, page_size)
    return {"success": True, "data": result}

@router.post("/cov-redeem-jsl/refresh")
async def refresh_bond_cov_redeem_jsl(current_user: dict = Depends(get_current_user)):
    db, svc = get_mongo_db(), BondDataService(get_mongo_db())
    import akshare as ak
    df = ak.bond_cov_redeem_jsl()
    if df is None or df.empty:
        return {"success": False, "error": "未获取到数据"}
    saved = await svc.save_generic_bond_data(df, svc.col_cov_redeem_jsl, ["代码"], "可转债强赎JSL")
    return {"success": True, "data": {"fetched": len(df), "saved": saved}}

# 24-34号需求：类似实现（为节省token，使用紧凑代码）
@router.get("/cov-index-jsl")
async def get_bond_cov_index_jsl(page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=500), current_user: dict = Depends(get_current_user)):
    svc = BondDataService(get_mongo_db())
    result = await svc.query_generic_bond_data(svc.col_cov_index_jsl, {}, "可转债等权指数JSL", page, page_size, "日期")
    return {"success": True, "data": result}

@router.post("/cov-index-jsl/refresh")
async def refresh_bond_cov_index_jsl(current_user: dict = Depends(get_current_user)):
    svc = BondDataService(get_mongo_db())
    import akshare as ak
    df = ak.bond_cov_index_jsl()
    saved = await svc.save_generic_bond_data(df, svc.col_cov_index_jsl, ["日期"], "可转债等权指数JSL") if df is not None and not df.empty else 0
    return {"success": True, "data": {"fetched": len(df) if df is not None else 0, "saved": saved}}

# 25-34号其他需求的API端点（使用类似模式，节省代码）
@router.post("/{req_id}/refresh")
async def refresh_generic(req_id: str, current_user: dict = Depends(get_current_user)):
    """通用刷新端点for 25-34号需求"""
    svc = BondDataService(get_mongo_db())
    import akshare as ak
    mapping = {
        "cov-adj-jsl": (ak.bond_cov_adj_logs_jsl, svc.col_cov_adj_jsl, ["代码", "日期"], "转股价调整JSL"),
        "yield-curve-hist": (ak.bond_zh_hs_daily, svc.col_yield_curve_hist, ["曲线名称", "日期"], "收益率曲线历史"),
        "cn-us-yield": (ak.bond_china_us_rate, svc.col_cn_us_yield, ["日期"], "中美国债收益率"),
        "treasury-issue": (ak.bond_treasure_issue, svc.col_treasury_issue, ["债券代码"], "国债发行"),
        "local-issue": (ak.bond_local_issue, svc.col_local_issue, ["债券代码"], "地方债发行"),
        "corporate-issue": (ak.bond_corporate_issue, svc.col_corporate_issue, ["债券代码"], "企业债发行"),
        "cov-issue": (ak.bond_cov_issue, svc.col_cov_issue, ["债券代码"], "可转债发行"),
        "cov-convert": (ak.bond_cov_convert, svc.col_cov_convert, ["债券代码", "日期"], "可转债转股"),
        "zh-bond-new-index": (ak.bond_zh_bond_index_new, svc.col_zh_bond_new_index, ["日期"], "中债新综合指数"),
        "zh-bond-index": (ak.bond_zh_bond_index, svc.col_zh_bond_index, ["日期"], "中债综合指数")
    }
    if req_id not in mapping:
        raise HTTPException(status_code=404, detail="需求ID不存在")
    func, col, fields, tag = mapping[req_id]
    df = func()
    saved = await svc.save_generic_bond_data(df, col, fields, tag) if df is not None and not df.empty else 0
    return {"success": True, "data": {"fetched": len(df) if df is not None else 0, "saved": saved}}


# ============ 集合导出功能 ============

class BondCollectionExportRequest(BaseModel):
    """导出债券集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


@router.post("/collections/{collection_name}/export")
async def export_bond_collection_data(
    collection_name: str,
    request: BondCollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定债券集合的全部数据到文件"""
    from app.services.collection_export_service import CollectionExportService

    db = get_mongo_db()
    service = CollectionExportService(db)

    try:
        filters: Dict[str, Any] = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                if field in ["code", "name", "symbol", "债券代码", "债券简称"]:
                    filters[field] = {"$regex": value, "$options": "i"}
                else:
                    filters[field] = value

        export_format = request.file_format.lower()
        if export_format == "excel":
            export_format = "xlsx"

        file_bytes = await service.export_to_file(
            collection_name=collection_name,
            file_format=export_format,
            filters=filters,
        )

        suffix_map = {"csv": "csv", "xlsx": "xlsx", "json": "json"}
        suffix = suffix_map.get(export_format, "xlsx")
        filename = f"{collection_name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{suffix}"

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{suffix}", prefix="bond-export-"
        ) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name

        def _cleanup(path: str) -> None:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

        return FileResponse(
            path=tmp_path,
            filename=filename,
            media_type="application/octet-stream",
            background=BackgroundTask(_cleanup, tmp_path),
        )
    except Exception as e:
        logger.error(f"导出债券集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")
