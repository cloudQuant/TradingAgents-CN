from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query

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
    db = get_mongo_db()
    # 规范参数：每页最多20条；排序方向仅允许 asc/desc
    try:
        page_size = max(1, min(int(page_size), 20))
    except Exception:
        page_size = 20
    sdir = str(sort_dir or "asc").lower()
    if sdir not in ("asc", "desc"):
        sdir = "asc"
    sort_dir = sdir
    # 如果category为空或None，不设置默认值，查询所有类别
    # 注意：这里不再强制设置默认值，让前端控制默认显示
    if category and category.strip() == "":
        category = None
    svc = BondDataService(db)
    await svc.ensure_indexes()

    # 先从数据库查询
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

    # 如果库里没有，则回退到 AKShare，拉取后保存再查询一次
    if total == 0:
        provider = AKShareBondProvider()
        fetched = await provider.get_symbol_list()
        if fetched:
            await svc.save_basic_list(fetched)
            # 重新查询，确保使用正确的分页、排序和过滤
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

    # 移除 _id，避免序列化问题
    for it in items:
        if isinstance(it, dict) and it.get("_id") is not None:
            it.pop("_id", None)

    # 兼容 limit（若调用方仍传入limit，则仍然生效于当前页上限）
    if limit and len(items) > limit:
        items = items[:limit]

    return {"success": True, "data": {"total": total, "page": page, "page_size": page_size, "items": items}}


@router.get("/{code}/history")
async def get_bond_history(
    code: str,
    start: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end: str = Query(..., description="结束日期 YYYY-MM-DD"),
    period: str = Query("daily", description="周期，默认 daily"),
    current_user: dict = Depends(get_current_user),
):
    result = get_cn_bond_data_unified(code, start, end, period)
    return {"success": not result.startswith("❌"), "data": result}


@router.get("/{code}/analytics")
async def get_bond_analytics(
    code: str,
    start: str = Query(..., description="开始日期 YYYY-MM-DD"),
    end: str = Query(..., description="结束日期 YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user),
):
    # 现阶段的分析结果随历史数据字符串一起包含（含MA/MACD/RSI/BOLL等），先复用
    result = get_cn_bond_data_unified(code, start, end, period="daily")
    return {"success": not result.startswith("❌"), "data": result}


@router.get("/{code}/info")
async def get_bond_info(
    code: str,
    current_user: dict = Depends(get_current_user),
):
    info = get_cn_bond_info_unified(code)
    ok = isinstance(info, dict) and not info.get("error")
    return {"success": ok, "data": info}


@router.get("/yield-curve")
async def get_bond_yield_curve(
    start: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD，可选"),
    end: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD，可选"),
    current_user: dict = Depends(get_current_user),
):
    result = get_cn_bond_yield_curve_unified(start, end)
    return {"success": not result.startswith("❌"), "data": result}


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
