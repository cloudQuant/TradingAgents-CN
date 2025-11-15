from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
import hashlib
import logging
import uuid
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

router = APIRouter(prefix="/api/bonds", tags=["bonds"])
logger = logging.getLogger("webapi")  # 使用与其他路由一致的日志器

# 简单的内存缓存，用于减少数据库查询
_bond_list_cache = {}
_cache_ttl_seconds = 300  # 5分钟缓存

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
            logger.warning(f"⚠️ [债券列表] 数据库为空 (total=0)，将从 AKShare 获取数据并保存到数据库 (category={category})")
            try:
                provider = AKShareBondProvider()
                fetched = await provider.get_symbol_list()
                if fetched:
                    logger.info(f"📡 [债券列表] 从 AKShare 获取到 {len(fetched)} 条债券数据，正在保存到数据库...")
                    saved_count = await svc.save_basic_list(fetched)
                    logger.info(f"💾 [债券列表] 已保存 {saved_count} 条债券数据到数据库")
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
            except Exception as e:
                logger.error(f"❌ [债券列表] 从 AKShare 获取数据失败: {e}", exc_info=True)
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
            "name": "bond_info_cm",
            "display_name": "中债信息",
            "description": "中国外汇交易中心债券信息，包括债券查询结果和详细信息",
            "route": "/bonds/collections/bond_info_cm",
            "fields": ["code", "endpoint", "债券简称", "债券代码", "发行人/受托机构", "债券类型"],
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
        
        # 获取字段信息（从第一条记录推断）
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


@router.post("/{code}/history/sync")
async def sync_bond_history_to_db(
    code: str,
    start: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end: str = Query(..., description="结束日期 YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user),
):
    provider = AKShareBondProvider()
    df = await provider.get_historical_data(code, start, end, period="daily")
    db = get_mongo_db()
    svc = BondDataService(db)
    await svc.ensure_indexes()
    norm = normalize_bond_code(code)
    code_std = norm.get("code_std") or code
    saved = await svc.save_bond_daily(code_std, df)
    return {"success": True, "data": {"saved": saved, "rows": 0 if df is None else len(df)}}
