"""
债券数据集合路由
参考 funds.py 重构，使用新架构
"""
from datetime import datetime, timedelta
import asyncio
import hashlib
import logging
import os
import tempfile
import uuid
from typing import Optional, Dict, Any, List

from fastapi import (
    APIRouter,
    Depends,
    Query,
    BackgroundTasks,
    HTTPException,
    status,
    Body,
    UploadFile,
    File,
)
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel

from app.routers.auth_db import get_current_user
from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.bond_refresh_service import BondRefreshService
from app.services.bond_data_service import BondDataService
from app.config.bond_update_config import get_collection_update_config
from app.services.data_sources.bonds.provider_registry import (
    get_collection_definitions,
    get_provider_class,
)
from app.schemas.bonds import (
    RefreshCollectionRequest,
    RefreshTaskResponse,
    ClearCollectionResponse,
    ApiResponse,
)
from app.exceptions.bonds import (
    BondCollectionNotFound,
    BondDataUpdateError,
    BondTaskNotFound,
)


class BondCollectionExportRequest(BaseModel):
    """导出债券集合请求"""
    file_format: str = "xlsx"  # csv, xlsx, json
    filter_field: Optional[str] = None
    filter_value: Optional[str] = None
    sort_by: Optional[str] = None
    sort_dir: str = "desc"


router = APIRouter(prefix="/api/bonds", tags=["bonds"])
logger = logging.getLogger("webapi")


def _get_collection_fields_order(collection_name: str) -> list:
    """获取集合的字段顺序，从 provider 的 field_info 获取"""
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                system_fields = {"更新时间", "更新人", "创建时间", "创建人", "来源"}
                fields = [f.get("name") for f in field_info 
                         if f.get("name") and f.get("name") not in system_fields]
                if fields:
                    return fields
    except Exception as e:
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
    return []


def _get_provider_field_info(collection_name: str) -> List[Dict[str, Any]]:
    """获取 provider 的完整字段信息"""
    try:
        provider_cls = get_provider_class(collection_name)
        if provider_cls:
            field_info = getattr(provider_cls, 'field_info', [])
            if field_info:
                return field_info
    except Exception as e:
        logger.warning(f"从 provider 获取字段信息失败 {collection_name}: {e}")
    return []


@router.get("/overview")
async def get_bonds_overview(current_user: dict = Depends(get_current_user)):
    """获取债券概览数据"""
    try:
        db = get_mongo_db()
        stats = {
            "total_bonds": 0,
            "categories": [],
            "message": "债券概览功能正在开发中"
        }
        return {"success": True, "data": stats}
    except Exception as e:
        logger.error(f"获取债券概览失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections")
async def list_bond_collections(
    current_user: dict = Depends(get_current_user)
):
    """获取债券数据集合列表"""
    try:
        collections = get_collection_definitions()
        return {
            "success": True,
            "data": collections,
            "total": len(collections),
        }
    except Exception as e:
        logger.error(f"获取集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/update-config")
async def get_collection_update_config_endpoint(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合的更新配置"""
    try:
        config = get_collection_update_config(collection_name)
        return {"success": True, "data": config}
    except Exception as e:
        logger.error(f"获取更新配置失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}")
async def get_collection_data(
    collection_name: str,
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(50, ge=1, le=500, description="每页数量"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_dir: str = Query("desc", description="排序方向：asc|desc"),
    filter_field: Optional[str] = Query(None, description="过滤字段"),
    filter_value: Optional[str] = Query(None, description="过滤值"),
    current_user: dict = Depends(get_current_user),
):
    """获取集合数据（分页）- 直接查询数据库，与 funds.py 一致"""
    db = get_mongo_db()
    
    # 验证集合是否存在
    supported_collections = [c["name"] for c in get_collection_definitions()]
    if collection_name not in supported_collections:
        raise BondCollectionNotFound(collection_name)
    
    # 直接获取集合
    collection = db.get_collection(collection_name)
    
    try:
        # 构建查询条件
        mongo_query = {}
        if filter_field and filter_value:
            filter_field_stripped = filter_field.strip()
            filter_value_stripped = filter_value.strip()
            if filter_field_stripped and filter_value_stripped:
                if filter_field_stripped in ["code", "name", "债券简称", "债券代码"]:
                    mongo_query[filter_field_stripped] = {"$regex": filter_value_stripped, "$options": "i"}
                else:
                    mongo_query[filter_field_stripped] = filter_value_stripped
        
        # 获取总数
        total = await collection.count_documents(mongo_query)
        
        # 构建排序
        sort_key = sort_by if sort_by else "_id"
        sort_direction = -1 if sort_dir == "desc" else 1
        
        # 分页查询
        skip = (page - 1) * page_size
        cursor = collection.find(mongo_query).sort(sort_key, sort_direction).skip(skip).limit(page_size)
        items = []
        
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)
        
        # 获取字段信息
        fields_info = []
        if items:
            sample = items[0]
            
            # 从 provider 获取完整的字段信息
            provider_field_info = _get_provider_field_info(collection_name)
            
            # 构建实际数据中的字段字典
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
            
            # 按 provider 的 field_info 顺序排列字段
            if provider_field_info:
                for field_def in provider_field_info:
                    field_name = field_def.get("name")
                    if field_name and field_name in fields_dict:
                        field_info = {
                            "name": field_name,
                            "type": field_def.get("type", fields_dict[field_name]["type"]),
                            "description": field_def.get("description", ""),
                            "example": fields_dict[field_name].get("example"),
                        }
                        fields_info.append(field_info)
                        del fields_dict[field_name]
                
                # 添加 provider 中未定义但实际数据中存在的字段
                for field_info in fields_dict.values():
                    fields_info.append(field_info)
            else:
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
    except BondCollectionNotFound:
        raise
    except Exception as e:
        logger.error(f"获取债券集合 {collection_name} 数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/stats")
async def get_collection_stats(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合统计信息"""
    db = get_mongo_db()
    refresh_service = BondRefreshService(db, current_user)
    
    try:
        overview = await refresh_service.get_collection_overview(collection_name)
        return {
            "success": True,
            "data": {
                "total_count": overview.get("total_count", 0),
                "collection_name": collection_name,
                "last_updated": overview.get("last_updated"),
            },
        }
    except BondCollectionNotFound as e:
        return {"success": False, "error": str(e.detail)}
    except Exception as e:
        logger.error(f"获取集合统计失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/refresh")
async def refresh_collection_data(
    collection_name: str,
    background_tasks: BackgroundTasks,
    request: RefreshCollectionRequest = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """刷新集合数据"""
    db = get_mongo_db()
    task_manager = get_task_manager()
    
    # create_task 返回 task_id，与 funds.py 保持一致
    task_id = task_manager.create_task(
        task_type=f"refresh_{collection_name}",
        description=f"更新债券集合: {collection_name}"
    )
    
    async def do_refresh():
        refresh_service = BondRefreshService(db, current_user)
        try:
            params = request.model_dump() if hasattr(request, 'model_dump') else request.dict()
            await refresh_service.refresh_collection(collection_name, task_id, params)
        except Exception as e:
            logger.error(f"刷新集合失败 {collection_name}: {e}", exc_info=True)
            task_manager.fail_task(task_id, str(e))
    
    background_tasks.add_task(do_refresh)
    
    # 与 funds.py 保持一致，使用 data 字段
    return RefreshTaskResponse(
        success=True,
        data={
            "task_id": task_id,
            "message": f"刷新任务已创建"
        }
    )


@router.get("/collections/refresh/task/{task_id}")
async def get_refresh_task_status(
    task_id: str,
    current_user: dict = Depends(get_current_user),
):
    """获取刷新任务状态"""
    task_manager = get_task_manager()
    task = task_manager.get_task(task_id)
    
    if not task:
        raise BondTaskNotFound(task_id)
    
    return {"success": True, "data": task}


@router.post("/collections/{collection_name}/upload")
async def upload_collection_data(
    collection_name: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """上传文件导入数据"""
    db = get_mongo_db()
    data_service = BondDataService(db)
    
    try:
        content = await file.read()
        result = await data_service.import_data_from_file(
            collection_name, content, file.filename
        )
        return result
    except Exception as e:
        logger.error(f"上传文件失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/collections/{collection_name}/sync")
async def sync_collection_from_remote(
    collection_name: str,
    config: Dict[str, Any] = Body(...),
    current_user: dict = Depends(get_current_user),
):
    """从远程数据库同步数据"""
    db = get_mongo_db()
    data_service = BondDataService(db)
    
    try:
        result = await data_service.sync_data_from_remote(collection_name, config)
        return result
    except Exception as e:
        logger.error(f"远程同步失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.delete("/collections/{collection_name}/clear")
async def clear_collection_data(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """清空集合数据"""
    db = get_mongo_db()
    refresh_service = BondRefreshService(db, current_user)
    
    try:
        result = await refresh_service.clear_collection(collection_name)
        return ClearCollectionResponse(
            success=True,
            data={
                "collection_name": collection_name,
                "deleted_count": result.get("deleted_count", 0),
                "dropped_indexes": result.get("dropped_indexes", 0),
                "message": result.get("message", "清空完成")
            }
        )
    except BondCollectionNotFound as e:
        return ClearCollectionResponse(success=False, data={}, error=str(e.detail))
    except Exception as e:
        logger.error(f"清空集合失败 {collection_name}: {e}", exc_info=True)
        return ClearCollectionResponse(success=False, data={}, error=str(e))


@router.get("/collections/{collection_name}/export")
async def export_collection_data(
    collection_name: str,
    file_format: str = Query("csv", description="导出格式: csv, xlsx, json"),
    current_user: dict = Depends(get_current_user),
):
    """导出集合数据"""
    db = get_mongo_db()
    data_service = BondDataService(db)
    
    try:
        content = await data_service.export_data_to_file(collection_name, file_format)
        
        suffix_map = {"csv": ".csv", "xlsx": ".xlsx", "json": ".json"}
        suffix = suffix_map.get(file_format.lower(), ".csv")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        filename = f"{collection_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{suffix}"
        
        return FileResponse(
            tmp_path,
            filename=filename,
            media_type="application/octet-stream",
            background=BackgroundTask(lambda: os.unlink(tmp_path)),
        )
    except Exception as e:
        logger.error(f"导出集合失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/collections/{collection_name}/overview")
async def get_collection_overview(
    collection_name: str,
    current_user: dict = Depends(get_current_user),
):
    """获取集合概览"""
    db = get_mongo_db()
    refresh_service = BondRefreshService(db, current_user)
    
    try:
        overview = await refresh_service.get_collection_overview(collection_name)
        return {"success": True, "data": overview}
    except BondCollectionNotFound as e:
        return {"success": False, "error": str(e.detail)}
    except Exception as e:
        logger.error(f"获取集合概览失败 {collection_name}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
