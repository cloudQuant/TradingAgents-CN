from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException, BackgroundTasks, Body
from fastapi.responses import JSONResponse, FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel
import logging
import pandas as pd
import io
import os
import tempfile
import akshare as ak
from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.services.currency_data_service import CurrencyDataService
from app.services.currency_refresh_service import CurrencyRefreshService
from app.config.currency_update_config import (
    get_collection_update_config,
    get_all_collection_update_configs,
)
from app.utils.task_manager import get_task_manager
from app.schemas.currencies import (
    CollectionStatsResponse,
    ClearCollectionResponse,
    ApiResponse,
)
from app.services.data_sources.currencies.provider_registry import (
    get_currency_collection_definitions,
)

router = APIRouter(prefix="/api/currencies", tags=["currencies"])
logger = logging.getLogger("webapi")

@router.get("/config")
async def get_currency_config(current_user: dict = Depends(get_current_user)):
    """Get currency configuration including default API key"""
    return {
        "success": True,
        "data": {
            "default_api_key": os.getenv("CURRENCYSCOOP_API_KEY", "")
        }
    }

@router.get("/collections")
async def list_currencies_collections(current_user: dict = Depends(get_current_user)):
    """获取外汇数据集合列表（动态）"""
    try:
        collection_items = []
        for meta in get_currency_collection_definitions():
            name = meta.get("name")
            if not name:
                continue

            field_info = meta.get("field_info") or []
            fields = [f.get("name") for f in field_info if f.get("name")]

            collection_items.append(
                {
                    "name": name,
                    "display_name": meta.get("display_name") or name,
                    "description": meta.get("description") or "",
                    "route": meta.get("route") or f"/currencies/collections/{name}",
                    "fields": fields,
                }
            )

        return {"success": True, "data": collection_items}
    except Exception as e:
        logger.error(f"获取货币集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

@router.get("/tool/convert")
async def tool_currency_convert(
    base: str = Query("USD", description="Base currency"),
    to: str = Query("CNY", description="Target currency"),
    amount: str = Query("10000", description="Amount"),
    api_key: str = Query(..., description="API Key for currencyscoop"),
    current_user: dict = Depends(get_current_user),
):
    """Real-time currency conversion tool"""
    try:
        import akshare as ak
        import asyncio
        logger.info(f"🔄 [Currency Tool] Converting: {amount} {base} -> {to}")
        
        try:
            # Run blocking AKShare call in thread pool
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                None, 
                lambda: ak.currency_convert(base=base, to=to, amount=amount, api_key=api_key)
            )
        except Exception as api_err:
             return {"success": False, "message": f"API call failed: {str(api_err)}"}
        
        if df is None or df.empty:
            return {"success": False, "message": "No data fetched from API"}
            
        # The result usually contains 'date', 'base', 'to', 'amount', 'value'
        data = df.to_dict(orient="records")[0]
        return {"success": True, "data": data}
        
    except Exception as e:
        logger.error(f"❌ [Currency Tool] Conversion failed: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


# ============== 统一刷新 API ==============

@router.get("/collections/{collection_name}/update-config")
async def get_currency_collection_update_config(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合的更新配置"""
    config = get_collection_update_config(collection_name)
    return {"success": True, "data": config}


@router.post("/collections/{collection_name}/refresh")
async def refresh_currency_collection(
    collection_name: str,
    background_tasks: BackgroundTasks,
    params: Dict[str, Any] = Body(default={}),
    current_user: dict = Depends(get_current_user),
):
    """刷新指定的外汇数据集合（异步任务）"""
    try:
        task_manager = get_task_manager()
        refresh_service = CurrencyRefreshService()

        # 创建任务（确保 TaskManager 中有记录，便于前端查询状态）
        task_id = task_manager.create_task(
            task_type=f"refresh_{collection_name}",
            description=f"刷新外汇集合: {collection_name}",
        )

        async def do_refresh():
            try:
                await refresh_service.refresh_collection(
                    collection_name=collection_name,
                    task_id=task_id,
                    params=params or {},
                )
            except Exception as e:
                logger.error(f"后台刷新任务失败: {e}", exc_info=True)
                try:
                    task_manager.fail_task(task_id, str(e))
                except Exception as inner_e:
                    logger.error(f"更新任务状态失败: {inner_e}", exc_info=True)

        # 后台执行刷新任务
        background_tasks.add_task(do_refresh)

        return {"success": True, "data": {"task_id": task_id}}
    except Exception as e:
        logger.error(f"刷新 {collection_name} 失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections/{collection_name}/refresh/status/{task_id}")
async def get_currency_refresh_task_status(
    collection_name: str,
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取指定集合刷新任务的状态"""
    try:
        task_manager = get_task_manager()
        task = task_manager.get_task(task_id)

        if task is None:
            return {"success": False, "message": f"Task {task_id} not found"}

        return {"success": True, "data": task}
    except Exception as e:
        logger.error(f"❌ [Currency Refresh] Failed to get task status: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_currency_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取货币集合统计信息（总数、最近更新时间）"""
    db = get_mongo_db()
    svc = CurrencyDataService(db)

    collection_map = {
        "currency_latest": svc.col_latest,
        "currency_history": svc.col_history,
        "currency_time_series": svc.col_time_series,
        "currency_currencies": svc.col_currencies,
        "currency_convert": svc.col_convert,
    }

    if collection_name not in collection_map:
        raise HTTPException(status_code=404, detail="Collection not found")

    col = collection_map[collection_name]
    total_count = await col.count_documents({})

    last_doc_list = await col.find({}).sort("updated_at", -1).limit(1).to_list(length=1)
    last_updated_raw = last_doc_list[0].get("updated_at") if last_doc_list else None

    last_updated_dt = None
    if isinstance(last_updated_raw, datetime):
        last_updated_dt = last_updated_raw
    elif isinstance(last_updated_raw, str):
        try:
            last_updated_dt = datetime.fromisoformat(last_updated_raw)
        except Exception:
            last_updated_dt = None

    stats = CollectionStatsResponse(
        collection_name=collection_name,
        total_count=total_count,
        last_updated=last_updated_dt,
        index_info=None,
    )
    data = stats.dict()
    # 兼容前端使用 latest_date 字段
    data["latest_date"] = (
        last_updated_dt.isoformat() if isinstance(last_updated_dt, datetime) else last_updated_raw
    )

    return {"success": True, "data": data}


@router.get("/collections/{collection_name}/data")
async def get_currency_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    sort_by: Optional[str] = Query(None),
    sort_dir: str = Query("desc", regex="^(asc|desc)$"),
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据（含字段信息）"""
    try:
        db = get_mongo_db()
        refresh_service = CurrencyRefreshService(db)

        # 基础数据
        skip = (page - 1) * page_size
        result = await refresh_service.get_collection_data(
            collection_name, skip=skip, limit=page_size, 
            sort_by=sort_by, sort_dir=sort_dir
        )
        items = result.get("data", [])
        total = result.get("total", 0)

        # 清理数据中的无效浮点数（NaN、Infinity）
        import math
        import json
        for item in items:
            for key, value in item.items():
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        item[key] = None

        # 从样本记录推断字段，并保留 provider 中定义的顺序
        fields_info = []
        
        # 动态从 service 的 provider 获取 field_info
        try:
            service = refresh_service.services.get(collection_name)  # type: ignore[attr-defined]
            provider_field_info = getattr(service.provider, "field_info", []) if service else []
        except Exception:
            provider_field_info = []

        if items:
            sample = items[0]

            # 构建实际字段字典
            tmp_fields: Dict[str, Dict[str, Any]] = {}
            for key, value in sample.items():
                if key == "_id":
                    continue
                field_type = type(value).__name__
                tmp_fields[key] = {
                    "name": key,
                    "type": field_type,
                    "example": str(value)[:50] if value is not None else None,
                }

            # 优先按 provider 的 field_info 顺序
            if provider_field_info:
                for f in provider_field_info:
                    fname = f.get("name")
                    if fname and fname in tmp_fields:
                        info = tmp_fields.pop(fname)
                        info["type"] = f.get("type", info["type"])
                        info["description"] = f.get("description", "")
                        fields_info.append(info)

                # 追加剩余字段（多为系统字段）
                fields_info.extend(tmp_fields.values())
            else:
                fields_info = list(tmp_fields.values())

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
        logger.error(f"❌ [Currency Collection] Failed to get data: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.get("/collections/{collection_name}/overview")
async def get_currency_collection_overview(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据概览"""
    try:
        db = get_mongo_db()
        refresh_service = CurrencyRefreshService(db)
        
        result = await refresh_service.get_collection_overview(collection_name)
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"❌ [Currency Collection] Failed to get overview: {e}", exc_info=True)
        return {"success": False, "message": str(e)}


@router.delete("/collections/{collection_name}")
async def clear_currency_collection(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
) -> ClearCollectionResponse:
    """清空指定货币集合的数据（统一接口）"""
    try:
        refresh_service = CurrencyRefreshService()
        supported = refresh_service.get_supported_collections()
        if collection_name not in supported:
            raise HTTPException(status_code=404, detail="Collection not found")

        result = await refresh_service.clear_collection(collection_name)
        deleted = int(result.get("deleted_count", 0)) if isinstance(result, dict) else 0

        return ClearCollectionResponse(
            success=bool(result.get("success", True)) if isinstance(result, dict) else True,
            message=result.get("message", "清空完成") if isinstance(result, dict) else "清空完成",
            deleted_count=deleted,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"清空货币集合失败: {e}", exc_info=True)
        return ClearCollectionResponse(success=False, message=str(e), deleted_count=0)


@router.post("/collections/{collection_name}/upload")
async def upload_currency_collection_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传货币集合数据文件（通用导入接口，占位实现）"""
    # 当前 currencies 集合全部来自 API，不强制实现文件导入逻辑，先简单返回错误提示
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "目前货币集合暂不支持文件导入，请使用 API 刷新功能",
        },
    )


@router.post("/collections/{collection_name}/sync")
async def sync_currency_collection_data(
    collection_name: str,
    config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
) -> ApiResponse:
    """远程同步货币集合数据（占位接口，用于前端统一 UI）"""
    # currencies 模块目前没有远程 MongoDB 同步的实际实现，这里直接返回错误信息，避免前端 404
    return ApiResponse(
        success=False,
        message="远程同步暂未在货币模块中实现，请使用 API 刷新或工具接口",
        data=None,
        error=None,
    )


# ============ 集合导出功能 ============

class CurrencyCollectionExportRequest(BaseModel):
    """导出外汇集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


@router.post("/collections/{collection_name}/export")
async def export_currency_collection_data(
    collection_name: str,
    request: CurrencyCollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定外汇集合的全部数据到文件"""
    from app.services.collection_export_service import CollectionExportService

    db = get_mongo_db()
    service = CollectionExportService(db)

    try:
        filters: Dict[str, Any] = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                if field in ["code", "name", "symbol", "currency"]:
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
            delete=False, suffix=f".{suffix}", prefix="currency-export-"
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
        logger.error(f"导出外汇集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")
