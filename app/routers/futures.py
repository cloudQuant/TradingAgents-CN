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
