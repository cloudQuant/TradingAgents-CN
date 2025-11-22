from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status, UploadFile, File
from pydantic import BaseModel
import hashlib
import logging
import uuid
import asyncio
from fastapi.responses import JSONResponse

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
        {
            "name": "bond_info_cm",
            "display_name": "债券信息查询",
            "description": "中国外汇交易中心债券信息查询，支持按债券名称、代码、发行人、债券类型、付息方式、发行年份、承销商、评级等条件查询",
            "route": "/bonds/collections/bond_info_cm",
            "fields": ["code", "债券简称", "债券代码", "发行人/受托机构", "债券类型", "发行日期", "最新债项评级", "查询代码"],
        },
        {
            "name": "bond_basic_info",
            "display_name": "债券基础信息",
            "description": "债券的基础信息，包括代码、名称、类别、发行人、息票率、上市日期、到期日等",
            "route": "/bonds/collections/bond_basic_info",
            "fields": ["code", "name", "exchange", "category", "issuer", "coupon_rate", "list_date", "maturity_date", "type"],
        },
        {
            "name": "bond_daily",
            "display_name": "债券历史行情",
            "description": "债券的历史行情数据，包括日期、开盘价、最高价、最低价、收盘价、成交量等",
            "route": "/bonds/collections/bond_daily",
            "fields": ["code", "date", "open", "high", "low", "close", "volume", "amount"],
        },
        {
            "name": "yield_curve_daily",
            "display_name": "收益率曲线",
            "description": "债券收益率曲线数据，包括日期、曲线名称、期限、收益率等",
            "route": "/bonds/collections/yield_curve_daily",
            "fields": ["date", "curve_name", "tenor", "yield", "yield_type"],
        },
        {
            "name": "bond_spot_quotes",
            "display_name": "债券现货报价",
            "description": "债券现货报价数据，包括最新价、涨跌额、涨跌幅、买入价、卖出价等",
            "route": "/bonds/collections/bond_spot_quotes",
            "fields": ["code", "timestamp", "category", "latest_price", "change", "change_percent", "buy", "sell", "volume", "amount"],
        },
        {
            "name": "bond_minute_quotes",
            "display_name": "债券分钟数据",
            "description": "债券分钟级分时行情数据，包括时间、开盘价、最高价、最低价、收盘价、成交量等",
            "route": "/bonds/collections/bond_minute_quotes",
            "fields": ["code", "datetime", "period", "open", "high", "low", "close", "volume", "amount"],
        },
        {
            "name": "bond_cb_profiles",
            "display_name": "可转债档案",
            "description": "可转债的详细档案信息，包括债券基本信息、转股条款、赎回条款等",
            "route": "/bonds/collections/bond_cb_profiles",
            "fields": ["code", "name", "provider", "endpoint"],
        },
        {
            "name": "bond_cb_valuation_daily",
            "display_name": "可转债估值",
            "description": "可转债的价值分析数据，包括日期、收盘价、纯债价值、转股价值、纯债溢价率、转股溢价率等",
            "route": "/bonds/collections/bond_cb_valuation_daily",
            "fields": ["code", "date", "close", "pure_bond_value", "convert_value", "pure_bond_premium", "convert_premium"],
        },
        {
            "name": "bond_cb_comparison",
            "display_name": "可转债比价表",
            "description": "可转债与正股的比价数据，包括转股价、转股价值、转股溢价率、强赎触发价、回售触发价等",
            "route": "/bonds/collections/bond_cb_comparison",
            "fields": ["code", "date", "convert_price", "convert_value", "convert_premium"],
        },
        {
            "name": "bond_cb_adjustments",
            "display_name": "可转债转股价格调整",
            "description": "可转债转股价格的调整记录，包括调整日期、调整前转股价、调整后转股价等",
            "route": "/bonds/collections/bond_cb_adjustments",
            "fields": ["code", "date", "before_price", "after_price"],
        },
        {
            "name": "bond_cb_redeems",
            "display_name": "可转债强赎",
            "description": "可转债的强制赎回信息，包括强赎触发价、强赎状态、强赎日期等",
            "route": "/bonds/collections/bond_cb_redeems",
            "fields": ["code", "redeem_price", "redeem_status", "redeem_date"],
        },
        {
            "name": "bond_issues",
            "display_name": "债券发行",
            "description": "债券发行公告信息，包括国债、地方债、企业债、可转债等各类债券的发行信息",
            "route": "/bonds/collections/bond_issues",
            "fields": ["code", "issue_type", "date", "issue_amount", "issue_price"],
        },
        {
            "name": "bond_buybacks",
            "display_name": "债券回购",
            "description": "债券回购数据，包括上交所和深交所的质押式回购行情",
            "route": "/bonds/collections/bond_buybacks",
            "fields": ["code", "exchange", "date", "price", "volume"],
        },
        {
            "name": "bond_buybacks_hist",
            "display_name": "债券回购历史",
            "description": "债券回购的历史数据",
            "route": "/bonds/collections/bond_buybacks_hist",
            "fields": ["exchange", "date", "price", "volume"],
        },
        {
            "name": "bond_indices_daily",
            "display_name": "债券指数",
            "description": "债券指数数据，包括中债综合指数、中债新综合指数、集思录可转债等权指数等",
            "route": "/bonds/collections/bond_indices_daily",
            "fields": ["index_id", "date", "value"],
        },
        {
            "name": "us_yield_daily",
            "display_name": "美国国债收益率",
            "description": "中美国债收益率历史数据，包括2年、5年、10年、30年等期限的收益率",
            "route": "/bonds/collections/us_yield_daily",
            "fields": ["date", "tenor", "yield"],
        },
        {
            "name": "bond_spot_quote_detail",
            "display_name": "现货报价明细",
            "description": "银行间市场现券报价明细，包括报价机构、债券简称、买入净价、卖出净价等",
            "route": "/bonds/collections/bond_spot_quote_detail",
            "fields": ["code", "timestamp", "报价机构", "买入净价", "卖出净价", "买入收益率", "卖出收益率"],
        },
        {
            "name": "bond_spot_deals",
            "display_name": "现货成交明细",
            "description": "银行间市场现券成交明细，包括债券简称、成交净价、最新收益率、涨跌等",
            "route": "/bonds/collections/bond_spot_deals",
            "fields": ["code", "timestamp", "成交净价", "最新收益率", "涨跌", "加权收益率", "交易量"],
        },
        {
            "name": "bond_deal_summary",
            "display_name": "成交概览",
            "description": "上交所债券成交概览，包括债券类型、当日成交笔数、当日成交金额等",
            "route": "/bonds/collections/bond_deal_summary",
            "fields": ["date", "债券类型", "当日成交笔数", "当日成交金额", "当年成交笔数", "当年成交金额"],
        },
        {
            "name": "bond_cash_summary",
            "display_name": "现券市场概览",
            "description": "上交所债券现券市场概览，包括债券现货、托管只数、托管市值、托管面值等",
            "route": "/bonds/collections/bond_cash_summary",
            "fields": ["date", "债券现货", "托管只数", "托管市值", "托管面值"],
        },
        {
            "name": "bond_nafmii_debts",
            "display_name": "银行间市场债务",
            "description": "银行间市场非金融企业债务融资工具注册信息，包括债券名称、品种、金额、注册通知书文号等",
            "route": "/bonds/collections/bond_nafmii_debts",
            "fields": ["code", "债券名称", "品种", "金额", "注册通知书文号", "更新日期", "项目状态"],
        },
        {
            "name": "bond_cov_list",
            "display_name": "可转债列表",
            "description": "东方财富可转债数据一览表，包括债券代码、债券简称、申购日期、转股价等",
            "route": "/bonds/collections/bond_cov_list",
            "fields": ["code", "债券代码", "债券简称", "申购日期", "转股价", "转股价值", "转股溢价率"],
        },
        {
            "name": "bond_cb_list_jsl",
            "display_name": "集思录可转债",
            "description": "集思录可转债实时数据，包括行情数据和基本信息",
            "route": "/bonds/collections/bond_cb_list_jsl",
            "fields": ["code", "转债名称", "现价", "涨跌幅", "转股价", "转股价值", "转股溢价率"],
        },
        {
            "name": "bond_cb_summary",
            "display_name": "可转债债券概况",
            "description": "新浪财经可转债债券概况数据",
            "route": "/bonds/collections/bond_cb_summary",
            "fields": ["code", "债券类型", "票面利率", "发行价格", "发行规模", "到期日期"],
        },
        {
            "name": "bond_events",
            "display_name": "债券事件",
            "description": "债券相关事件记录，包括调整、赎回、付息等各类事件",
            "route": "/bonds/collections/bond_events",
            "fields": ["code", "date", "event_type", "description"],
        },
        {
            "name": "yield_curve_map",
            "display_name": "收益率曲线映射",
            "description": "收益率曲线可视化映射数据，用于收益率曲线的图形展示",
            "route": "/bonds/collections/yield_curve_map",
            "fields": ["date", "曲线数据"],
        },
    ]
    return {"success": True, "data": collections}


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
    
    # 获取集合
    collection_map = {
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
        "bond_buybacks_hist": svc.col_buybacks_hist,
        "bond_indices_daily": svc.col_indices,
        "us_yield_daily": svc.col_us_yield,
        "bond_spot_quote_detail": svc.col_spot_quote_detail,
        "bond_spot_deals": svc.col_spot_deals,
        "bond_deal_summary": svc.col_deal_summary,
        "bond_cash_summary": svc.col_cash_summary,
        "bond_nafmii_debts": svc.col_nafmii,
        "bond_info_cm": svc.col_info_cm,
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
    
    collection_map = {
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
        "bond_buybacks_hist": svc.col_buybacks_hist,
        "bond_indices_daily": svc.col_indices,
        "us_yield_daily": svc.col_us_yield,
        "bond_spot_quote_detail": svc.col_spot_quote_detail,
        "bond_spot_deals": svc.col_spot_deals,
        "bond_deal_summary": svc.col_deal_summary,
        "bond_cash_summary": svc.col_cash_summary,
        "bond_nafmii_debts": svc.col_nafmii,
        "bond_info_cm": svc.col_info_cm,
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
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD（可选，仅适用于某些集合）"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD（可选，仅适用于某些集合）"),
    date: Optional[str] = Query(None, description="指定日期 YYYY-MM-DD（可选，用于单日期集合）"),
    # bond_info_cm 特定参数
    bond_name: Optional[str] = Query(None, description="债券名称（bond_info_cm专用）"),
    bond_code: Optional[str] = Query(None, description="债券代码（bond_info_cm专用）"),
    bond_issue: Optional[str] = Query(None, description="发行人（bond_info_cm专用）"),
    bond_type: Optional[str] = Query(None, description="债券类型（bond_info_cm专用）"),
    coupon_type: Optional[str] = Query(None, description="付息方式（bond_info_cm专用）"),
    issue_year: Optional[str] = Query(None, description="发行年份（bond_info_cm专用）"),
    underwriter: Optional[str] = Query(None, description="承销商（bond_info_cm专用）"),
    grade: Optional[str] = Query(None, description="评级（bond_info_cm专用）"),
    current_user: dict = Depends(get_current_user),
):
    """从AKShare更新指定集合的数据（异步执行，支持进度查询）
    
    支持的参数因集合而异：
    - bond_info_cm: 支持 bond_name, bond_code, bond_issue, bond_type, coupon_type, issue_year, underwriter, grade
    - yield_curve_daily, bond_daily: 支持 start_date, end_date
    - bond_cash_summary, bond_deal_summary: 支持 date
    """
    try:
        logger.info(f"🔄 创建集合更新任务: {collection_name}")
        
        db = get_mongo_db()
        svc = BondDataService(db)
        refresh_service = CollectionRefreshService(svc)
        task_manager = get_task_manager()
        
        # 准备参数字典
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "date": date,
            "bond_name": bond_name,
            "bond_code": bond_code,
            "bond_issue": bond_issue,
            "bond_type": bond_type,
            "coupon_type": coupon_type,
            "issue_year": issue_year,
            "underwriter": underwriter,
            "grade": grade,
        }
        
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
