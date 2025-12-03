"""
Sync router for data synchronization
- Stock basics sync
- Collection sync between nodes (push/pull)
"""
from __future__ import annotations

import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Body, Header, Depends

from app.services.basics_sync_service import get_basics_sync_service
from app.services.collection_sync_service import get_sync_service

logger = logging.getLogger("webapi")

router = APIRouter(prefix="/api/sync", tags=["sync"])


# ==================== Stock Basics Sync ====================

@router.post("/stock_basics/run")
async def run_stock_basics_sync(force: bool = False):
    try:
        service = get_basics_sync_service()
        result = await service.run_full_sync(force=force)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock_basics/status")
async def get_stock_basics_status():
    service = get_basics_sync_service()
    status = await service.get_status()
    return {"success": True, "data": status}


# ==================== Ping (for node connection test) ====================

@router.get("/ping")
async def ping():
    """节点连接测试"""
    return {
        "success": True,
        "version": "1.0.0",
        "node_name": "TradingAgents-CN"
    }


# ==================== Node Management ====================

@router.get("/nodes")
async def get_nodes():
    """获取所有同步节点"""
    try:
        service = get_sync_service()
        nodes = await service.get_nodes()
        return {"success": True, "data": nodes}
    except Exception as e:
        logger.error(f"获取节点列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/nodes/{node_id}")
async def get_node(node_id: str):
    """获取单个节点"""
    try:
        service = get_sync_service()
        node = await service.get_node(node_id)
        if not node:
            return {"success": False, "error": "节点不存在"}
        return {"success": True, "data": node}
    except Exception as e:
        logger.error(f"获取节点失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/nodes")
async def create_node(node_data: Dict[str, Any] = Body(...)):
    """创建同步节点"""
    try:
        service = get_sync_service()
        node = await service.create_node(node_data)
        return {"success": True, "data": node}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"创建节点失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.put("/nodes/{node_id}")
async def update_node(node_id: str, node_data: Dict[str, Any] = Body(...)):
    """更新同步节点"""
    try:
        service = get_sync_service()
        node = await service.update_node(node_id, node_data)
        if not node:
            return {"success": False, "error": "节点不存在"}
        return {"success": True, "data": node}
    except Exception as e:
        logger.error(f"更新节点失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.delete("/nodes/{node_id}")
async def delete_node(node_id: str):
    """删除同步节点"""
    try:
        service = get_sync_service()
        success = await service.delete_node(node_id)
        if not success:
            return {"success": False, "error": "节点不存在"}
        return {"success": True, "message": "节点已删除"}
    except Exception as e:
        logger.error(f"删除节点失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/nodes/{node_id}/test")
async def test_node_connection(node_id: str):
    """测试节点连接"""
    try:
        service = get_sync_service()
        result = await service.test_node_connection(node_id)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"测试节点连接失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== Sync Tasks ====================

@router.get("/tasks")
async def get_tasks(limit: int = 50, skip: int = 0):
    """获取同步任务列表"""
    try:
        service = get_sync_service()
        tasks = await service.get_tasks(limit, skip)
        return {"success": True, "data": tasks}
    except Exception as e:
        logger.error(f"获取任务列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """获取单个任务状态"""
    try:
        service = get_sync_service()
        task = await service.get_task(task_id)
        if not task:
            return {"success": False, "error": "任务不存在"}
        return {"success": True, "data": task}
    except Exception as e:
        logger.error(f"获取任务失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== Sync Operations ====================

@router.post("/pull")
async def pull_data(
    source_node: str = Body(...),
    collection: str = Body(...),
    strategy: str = Body("incremental"),
    filter: Dict[str, Any] = Body(None)
):
    """从远程节点拉取数据"""
    try:
        service = get_sync_service()
        task = await service.pull_data(source_node, collection, strategy, filter)
        return {"success": True, "data": task}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"拉取数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@router.post("/push")
async def push_data(
    target_node: str = Body(...),
    collection: str = Body(...),
    strategy: str = Body("incremental"),
    filter: Dict[str, Any] = Body(None)
):
    """推送数据到远程节点"""
    try:
        service = get_sync_service()
        task = await service.push_data(target_node, collection, strategy, filter)
        return {"success": True, "data": task}
    except ValueError as e:
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"推送数据失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== Data Transfer API (for remote nodes) ====================

def verify_api_key(x_sync_api_key: Optional[str] = Header(None)):
    """验证 API Key（简化版，实际应从配置读取）"""
    # TODO: 从配置读取允许的 API Key
    # 目前暂时允许所有请求
    return True


@router.post("/data/export")
async def export_data(
    collection: str = Body(...),
    filter: Dict[str, Any] = Body(None),
    skip: int = Body(0),
    limit: int = Body(5000),
    _: bool = Depends(verify_api_key)
):
    """导出集合数据（供远程节点拉取）"""
    try:
        service = get_sync_service()
        result = await service.export_collection_data(collection, filter, skip, limit)
        return result
    except Exception as e:
        logger.error(f"导出数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/import")
async def import_data(
    collection: str = Body(...),
    data: List[Dict[str, Any]] = Body(...),
    unique_keys: List[str] = Body(None),
    mode: str = Body("upsert"),
    _: bool = Depends(verify_api_key)
):
    """导入集合数据（供远程节点推送）"""
    try:
        service = get_sync_service()
        result = await service.import_collection_data(collection, data, unique_keys, mode)
        return result
    except Exception as e:
        logger.error(f"导入数据失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/stats")
async def get_collection_stats(
    collection: str = Body(...),
    _: bool = Depends(verify_api_key)
):
    """获取集合统计信息（供远程节点查询）"""
    try:
        service = get_sync_service()
        result = await service.get_collection_stats(collection)
        return result
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Collections ====================

@router.get("/collections")
async def get_available_collections():
    """获取可同步的集合列表"""
    try:
        service = get_sync_service()
        collections = await service.get_available_collections()
        return {"success": True, "data": collections}
    except Exception as e:
        logger.error(f"获取集合列表失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

