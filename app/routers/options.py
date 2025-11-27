from typing import Optional, Dict, Any
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
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.option_data_service import OptionDataService
from app.services.option_refresh_service import OptionRefreshService
from app.config.option_update_config import OPTION_UPDATE_CONFIGS, get_collection_config

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
    """获取期权数据集合列表
    
    从配置文件动态生成集合列表，同时保留通用集合。
    """
    try:
        # 通用集合（非akshare数据源）
        base_collections = [
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
        ]
        
        # 从配置文件动态生成集合列表
        config_collections = []
        for name, config in OPTION_UPDATE_CONFIGS.items():
            config_collections.append({
                "name": name,
                "display_name": config.get("display_name", name),
                "description": config.get("update_description", ""),
                "route": f"/options/collections/{name}",
                "fields": [],  # 字段信息可从数据库动态获取
                "update_config": {
                    "single_update": config.get("single_update", {}),
                    "batch_update": config.get("batch_update", {})
                }
            })
        
        # 合并列表
        collections = base_collections + config_collections
        
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
    """获取指定期权集合的数据（分页）
    
    动态获取集合，支持所有配置的期权数据集合。
    """
    db = get_mongo_db()
    
    # 基础集合列表（非akshare数据源）
    base_collections = ["options_basic_info", "options_daily_quotes", "options_greeks"]
    
    # 验证集合是否存在（从配置或基础集合）
    if collection_name not in base_collections and collection_name not in OPTION_UPDATE_CONFIGS:
        return {"success": False, "error": f"集合 {collection_name} 不存在"}
    
    # 动态获取集合
    collection = db.get_collection(collection_name)
    
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
    params: Optional[Dict[str, Any]] = Body(default=None),
    current_user: dict = Depends(get_current_user),
):
    """刷新期权集合数据
    
    使用新的 OptionRefreshService 架构，支持所有已配置的期权数据集合。
    可通过 params 传递更新参数（如日期、品种代码等）。
    """
    try:
        db = get_mongo_db()
        task_manager = get_task_manager()
        refresh_service = OptionRefreshService(db, task_manager)
        
        # 检查集合是否支持
        config = get_collection_config(collection_name)
        if not config:
            # 回退到旧服务
            old_service = OptionDataService(db)
            method_name = f"fetch_and_save_{collection_name}"
            if hasattr(old_service, method_name):
                background_tasks.add_task(getattr(old_service, method_name))
                return {"success": True, "message": "数据刷新任务已提交", "status": "processing"}
            return {"success": False, "error": f"不支持刷新集合 {collection_name}"}
        
        # 创建任务
        task_id = str(uuid.uuid4())
        await task_manager.create_task(
            task_id=task_id,
            task_type="option_refresh",
            description=f"刷新期权数据: {config['display_name']}"
        )
        
        # 后台执行刷新任务
        async def do_refresh():
            try:
                update_params = params or {}
                result = await refresh_service.refresh_collection(
                    collection_name=collection_name,
                    task_id=task_id,
                    update_type="batch",
                    **update_params
                )
                return result
            except Exception as e:
                logger.error(f"刷新任务执行失败: {e}")
                await task_manager.update_task(task_id, status="failed", message=str(e))
        
        background_tasks.add_task(do_refresh)
        
        return {
            "success": True,
            "message": "数据刷新任务已提交",
            "status": "processing",
            "task_id": task_id
        }
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
    """清空期权集合数据
    
    使用 OptionRefreshService 统一处理所有集合的清空操作。
    """
    try:
        db = get_mongo_db()
        task_manager = get_task_manager()
        refresh_service = OptionRefreshService(db, task_manager)
        
        # 使用统一的清空方法
        result = await refresh_service.clear_collection(collection_name)
        
        if result.get("success"):
            return {
                "success": True,
                "message": result.get("message", f"已清空 {result.get('deleted_count', 0)} 条数据")
            }
        else:
            return {"success": False, "error": result.get("message", "清空失败")}
            
    except Exception as e:
        logger.error(f"清空期权集合 {collection_name} 失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_options_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取期权集合的统计信息
    
    使用 OptionRefreshService 统一获取统计信息。
    """
    try:
        db = get_mongo_db()
        task_manager = get_task_manager()
        refresh_service = OptionRefreshService(db, task_manager)
        
        # 使用统一的统计方法
        stats = await refresh_service.get_collection_stats(collection_name)
        
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


# ============ 集合导出功能 ============

class OptionCollectionExportRequest(BaseModel):
    """导出期权集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


@router.post("/collections/{collection_name}/export")
async def export_option_collection_data(
    collection_name: str,
    request: OptionCollectionExportRequest,
    current_user: dict = Depends(get_current_user),
):
    """导出指定期权集合的全部数据到文件"""
    from app.services.collection_export_service import CollectionExportService

    db = get_mongo_db()
    service = CollectionExportService(db)

    try:
        filters: Dict[str, Any] = {}
        if request.filter_field and request.filter_value:
            field = request.filter_field.strip()
            value = request.filter_value.strip()
            if field and value:
                if field in ["code", "name", "symbol"]:
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
            delete=False, suffix=f".{suffix}", prefix="option-export-"
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
        logger.error(f"导出期权集合 {collection_name} 数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")
