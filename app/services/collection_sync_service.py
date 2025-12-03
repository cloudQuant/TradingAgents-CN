"""
数据集合同步服务
支持任意两个节点之间的集合级别推送/拉取
"""
import logging
import uuid
import hashlib
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
import httpx
from bson import ObjectId

logger = logging.getLogger("webapi")


class CollectionSyncService:
    """数据集合同步服务"""
    
    # 集合同步配置 - 定义各集合的唯一键和增量字段
    COLLECTION_CONFIG = {
        # 股票相关
        "stock_info": {"unique_keys": ["ts_code"], "incremental_field": None, "chunk_size": 2000},
        "stock_daily_kline": {"unique_keys": ["ts_code", "trade_date"], "incremental_field": "trade_date", "chunk_size": 5000},
        "stock_weekly_kline": {"unique_keys": ["ts_code", "trade_date"], "incremental_field": "trade_date", "chunk_size": 5000},
        "stock_monthly_kline": {"unique_keys": ["ts_code", "trade_date"], "incremental_field": "trade_date", "chunk_size": 5000},
        
        # 基金相关
        "fund_basic_info": {"unique_keys": ["fund_code"], "incremental_field": None, "chunk_size": 1000},
        "fund_name_em": {"unique_keys": ["基金代码"], "incremental_field": None, "chunk_size": 2000},
        "fund_nav_history": {"unique_keys": ["fund_code", "nav_date"], "incremental_field": "nav_date", "chunk_size": 5000},
        
        # 债券相关
        "bond_info": {"unique_keys": ["bond_code"], "incremental_field": None, "chunk_size": 2000},
        "bond_info_cm": {"unique_keys": ["债券代码"], "incremental_field": None, "chunk_size": 2000},
        
        # 期货相关
        "futures_basic_info": {"unique_keys": ["symbol"], "incremental_field": None, "chunk_size": 1000},
        "futures_daily_kline": {"unique_keys": ["symbol", "trade_date"], "incremental_field": "trade_date", "chunk_size": 5000},
        
        # 期权相关
        "option_basic_info": {"unique_keys": ["ts_code"], "incremental_field": None, "chunk_size": 2000},
        
        # 外汇相关
        "currency_exchange_rate": {"unique_keys": ["currency_pair", "date"], "incremental_field": "date", "chunk_size": 5000},
    }
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.nodes_collection = db.get_collection("sync_nodes")
        self.tasks_collection = db.get_collection("sync_tasks")
        self.meta_collection = db.get_collection("sync_collection_meta")
        
    # ==================== 节点管理 ====================
    
    async def get_nodes(self) -> List[Dict[str, Any]]:
        """获取所有同步节点"""
        cursor = self.nodes_collection.find({}).sort("created_at", -1)
        nodes = await cursor.to_list(length=None)
        for node in nodes:
            node["_id"] = str(node["_id"])
            # 隐藏 API Key
            if node.get("api_key"):
                node["api_key_masked"] = node["api_key"][:8] + "****"
        return nodes
    
    async def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """获取单个节点"""
        node = await self.nodes_collection.find_one({"node_id": node_id})
        if node:
            node["_id"] = str(node["_id"])
        return node
    
    async def create_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建同步节点"""
        now = datetime.utcnow()
        node = {
            "node_id": node_data.get("node_id") or str(uuid.uuid4())[:8],
            "name": node_data["name"],
            "url": node_data["url"].rstrip("/"),
            "api_key": node_data.get("api_key", ""),
            "description": node_data.get("description", ""),
            "tags": node_data.get("tags", []),
            "status": "active",
            "last_sync_at": None,
            "created_at": now,
            "updated_at": now,
        }
        
        # 检查 node_id 是否已存在
        existing = await self.nodes_collection.find_one({"node_id": node["node_id"]})
        if existing:
            raise ValueError(f"节点ID '{node['node_id']}' 已存在")
        
        result = await self.nodes_collection.insert_one(node)
        node["_id"] = str(result.inserted_id)
        return node
    
    async def update_node(self, node_id: str, node_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新同步节点"""
        update_data = {
            "updated_at": datetime.utcnow()
        }
        for key in ["name", "url", "api_key", "description", "tags", "status"]:
            if key in node_data:
                update_data[key] = node_data[key]
        
        if "url" in update_data:
            update_data["url"] = update_data["url"].rstrip("/")
        
        result = await self.nodes_collection.find_one_and_update(
            {"node_id": node_id},
            {"$set": update_data},
            return_document=True
        )
        if result:
            result["_id"] = str(result["_id"])
        return result
    
    async def delete_node(self, node_id: str) -> bool:
        """删除同步节点"""
        result = await self.nodes_collection.delete_one({"node_id": node_id})
        return result.deleted_count > 0
    
    async def test_node_connection(self, node_id: str) -> Dict[str, Any]:
        """测试节点连接"""
        node = await self.get_node(node_id)
        if not node:
            return {"success": False, "error": "节点不存在"}
        
        try:
            start_time = datetime.utcnow()
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {}
                if node.get("api_key"):
                    headers["X-Sync-API-Key"] = node["api_key"]
                
                response = await client.get(
                    f"{node['url']}/api/sync/ping",
                    headers=headers
                )
                
                latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "latency_ms": round(latency_ms, 2),
                        "version": data.get("version", "unknown"),
                        "node_name": data.get("node_name", "unknown")
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "latency_ms": round(latency_ms, 2)
                    }
        except httpx.TimeoutException:
            return {"success": False, "error": "连接超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 同步任务管理 ====================
    
    async def get_tasks(self, limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        """获取同步任务列表"""
        cursor = self.tasks_collection.find({}).sort("started_at", -1).skip(skip).limit(limit)
        tasks = await cursor.to_list(length=None)
        for task in tasks:
            task["_id"] = str(task["_id"])
        return tasks
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取单个任务"""
        task = await self.tasks_collection.find_one({"task_id": task_id})
        if task:
            task["_id"] = str(task["_id"])
        return task
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建同步任务"""
        now = datetime.utcnow()
        task = {
            "task_id": str(uuid.uuid4()),
            "direction": task_data["direction"],  # push/pull
            "source_node": task_data.get("source_node", "local"),
            "target_node": task_data.get("target_node", "local"),
            "collection": task_data["collection"],
            "filter": task_data.get("filter", {}),
            "strategy": task_data.get("strategy", "incremental"),
            "status": "pending",
            "stats": {
                "total_records": 0,
                "transferred": 0,
                "inserted": 0,
                "updated": 0,
                "failed": 0
            },
            "started_at": now,
            "completed_at": None,
            "error_message": None
        }
        await self.tasks_collection.insert_one(task)
        task["_id"] = str(task["_id"])
        return task
    
    async def update_task_status(
        self, 
        task_id: str, 
        status: str, 
        stats: Dict = None, 
        error: str = None
    ):
        """更新任务状态"""
        update_data = {"status": status}
        if stats:
            update_data["stats"] = stats
        if error:
            update_data["error_message"] = error
        if status in ["completed", "failed"]:
            update_data["completed_at"] = datetime.utcnow()
        
        await self.tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": update_data}
        )
    
    # ==================== 数据导出 API（供远程节点调用） ====================
    
    async def export_collection_data(
        self,
        collection_name: str,
        filter_query: Dict = None,
        skip: int = 0,
        limit: int = 5000
    ) -> Dict[str, Any]:
        """导出集合数据（供远程节点拉取）"""
        collection = self.db.get_collection(collection_name)
        query = filter_query or {}
        
        # 获取总数
        total = await collection.count_documents(query)
        
        # 获取数据
        cursor = collection.find(query, {"_id": 0}).skip(skip).limit(limit)
        data = await cursor.to_list(length=limit)
        
        # 序列化数据（处理 datetime 等特殊类型）
        serialized_data = self._serialize_data(data)
        
        # 计算校验和
        checksum = hashlib.md5(json.dumps(serialized_data, sort_keys=True, default=str).encode()).hexdigest()
        
        return {
            "data": serialized_data,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": skip + len(data) < total,
            "checksum": checksum
        }
    
    async def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """获取集合统计信息（供远程节点查询）"""
        collection = self.db.get_collection(collection_name)
        
        count = await collection.count_documents({})
        
        # 获取配置
        config = self.COLLECTION_CONFIG.get(collection_name, {})
        incremental_field = config.get("incremental_field")
        
        stats = {
            "collection": collection_name,
            "count": count,
            "latest_value": None,
            "oldest_value": None,
            "incremental_field": incremental_field
        }
        
        if incremental_field and count > 0:
            # 获取最新和最旧的值
            latest = await collection.find_one(
                {incremental_field: {"$exists": True}},
                sort=[(incremental_field, -1)]
            )
            oldest = await collection.find_one(
                {incremental_field: {"$exists": True}},
                sort=[(incremental_field, 1)]
            )
            if latest:
                stats["latest_value"] = str(latest.get(incremental_field))
            if oldest:
                stats["oldest_value"] = str(oldest.get(incremental_field))
        
        return stats
    
    # ==================== 数据导入 API（供远程节点调用） ====================
    
    async def import_collection_data(
        self,
        collection_name: str,
        data: List[Dict],
        unique_keys: List[str] = None,
        mode: str = "upsert"
    ) -> Dict[str, Any]:
        """导入集合数据（供远程节点推送）"""
        collection = self.db.get_collection(collection_name)
        
        # 获取配置
        config = self.COLLECTION_CONFIG.get(collection_name, {})
        if not unique_keys:
            unique_keys = config.get("unique_keys", [])
        
        inserted = 0
        updated = 0
        failed = 0
        
        if mode == "upsert" and unique_keys:
            # 使用 upsert 模式
            for doc in data:
                try:
                    filter_query = {k: doc.get(k) for k in unique_keys if k in doc}
                    if filter_query:
                        result = await collection.update_one(
                            filter_query,
                            {"$set": doc},
                            upsert=True
                        )
                        if result.upserted_id:
                            inserted += 1
                        elif result.modified_count > 0:
                            updated += 1
                    else:
                        # 没有唯一键，直接插入
                        await collection.insert_one(doc)
                        inserted += 1
                except Exception as e:
                    logger.error(f"导入记录失败: {e}")
                    failed += 1
        elif mode == "insert":
            # 直接插入
            try:
                result = await collection.insert_many(data, ordered=False)
                inserted = len(result.inserted_ids)
            except Exception as e:
                logger.error(f"批量插入失败: {e}")
                failed = len(data)
        elif mode == "replace":
            # 先清空再插入
            await collection.delete_many({})
            try:
                result = await collection.insert_many(data)
                inserted = len(result.inserted_ids)
            except Exception as e:
                logger.error(f"替换插入失败: {e}")
                failed = len(data)
        
        return {
            "inserted": inserted,
            "updated": updated,
            "failed": failed,
            "total": len(data)
        }
    
    # ==================== 同步操作 ====================
    
    async def pull_data(
        self,
        source_node_id: str,
        collection_name: str,
        strategy: str = "incremental",
        filter_query: Dict = None
    ) -> Dict[str, Any]:
        """从远程节点拉取数据到本地"""
        # 获取节点信息
        node = await self.get_node(source_node_id)
        if not node:
            raise ValueError(f"节点 '{source_node_id}' 不存在")
        
        # 创建任务
        task = await self.create_task({
            "direction": "pull",
            "source_node": source_node_id,
            "target_node": "local",
            "collection": collection_name,
            "filter": filter_query or {},
            "strategy": strategy
        })
        
        # 异步执行同步
        asyncio.create_task(self._execute_pull(task["task_id"], node, collection_name, strategy, filter_query))
        
        return task
    
    async def _execute_pull(
        self,
        task_id: str,
        node: Dict,
        collection_name: str,
        strategy: str,
        filter_query: Dict = None
    ):
        """执行拉取操作"""
        try:
            await self.update_task_status(task_id, "running")
            
            # 获取配置
            config = self.COLLECTION_CONFIG.get(collection_name, {})
            chunk_size = config.get("chunk_size", 5000)
            unique_keys = config.get("unique_keys", [])
            incremental_field = config.get("incremental_field")
            
            # 构建过滤条件
            query = filter_query or {}
            if strategy == "incremental" and incremental_field:
                local_stats = await self.get_collection_stats(collection_name)
                if local_stats.get("latest_value"):
                    query[incremental_field] = {"$gt": local_stats["latest_value"]}
            
            # 准备请求
            headers = {}
            if node.get("api_key"):
                headers["X-Sync-API-Key"] = node["api_key"]
            
            total_inserted = 0
            total_updated = 0
            total_records = 0
            skip = 0
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 先获取远程统计信息
                stats_response = await client.post(
                    f"{node['url']}/api/sync/data/stats",
                    headers=headers,
                    json={"collection": collection_name}
                )
                if stats_response.status_code == 200:
                    remote_stats = stats_response.json()
                    total_records = remote_stats.get("count", 0)
                
                # 分批拉取数据
                while True:
                    response = await client.post(
                        f"{node['url']}/api/sync/data/export",
                        headers=headers,
                        json={
                            "collection": collection_name,
                            "filter": query,
                            "skip": skip,
                            "limit": chunk_size
                        }
                    )
                    
                    if response.status_code != 200:
                        raise Exception(f"拉取数据失败: HTTP {response.status_code}")
                    
                    result = response.json()
                    data = result.get("data", [])
                    
                    if not data:
                        break
                    
                    # 导入数据
                    import_result = await self.import_collection_data(
                        collection_name,
                        data,
                        unique_keys,
                        "upsert"
                    )
                    
                    total_inserted += import_result["inserted"]
                    total_updated += import_result["updated"]
                    
                    # 更新进度
                    await self.update_task_status(task_id, "running", {
                        "total_records": total_records,
                        "transferred": skip + len(data),
                        "inserted": total_inserted,
                        "updated": total_updated,
                        "failed": import_result["failed"]
                    })
                    
                    if not result.get("has_more"):
                        break
                    
                    skip += chunk_size
            
            # 完成
            await self.update_task_status(task_id, "completed", {
                "total_records": total_records,
                "transferred": skip + len(data) if data else skip,
                "inserted": total_inserted,
                "updated": total_updated,
                "failed": 0
            })
            
            # 更新节点最后同步时间
            await self.nodes_collection.update_one(
                {"node_id": node["node_id"]},
                {"$set": {"last_sync_at": datetime.utcnow()}}
            )
            
        except Exception as e:
            logger.error(f"拉取数据失败: {e}", exc_info=True)
            await self.update_task_status(task_id, "failed", error=str(e))
    
    async def push_data(
        self,
        target_node_id: str,
        collection_name: str,
        strategy: str = "incremental",
        filter_query: Dict = None
    ) -> Dict[str, Any]:
        """将本地数据推送到远程节点"""
        # 获取节点信息
        node = await self.get_node(target_node_id)
        if not node:
            raise ValueError(f"节点 '{target_node_id}' 不存在")
        
        # 创建任务
        task = await self.create_task({
            "direction": "push",
            "source_node": "local",
            "target_node": target_node_id,
            "collection": collection_name,
            "filter": filter_query or {},
            "strategy": strategy
        })
        
        # 异步执行同步
        asyncio.create_task(self._execute_push(task["task_id"], node, collection_name, strategy, filter_query))
        
        return task
    
    async def _execute_push(
        self,
        task_id: str,
        node: Dict,
        collection_name: str,
        strategy: str,
        filter_query: Dict = None
    ):
        """执行推送操作"""
        try:
            await self.update_task_status(task_id, "running")
            
            # 获取配置
            config = self.COLLECTION_CONFIG.get(collection_name, {})
            chunk_size = config.get("chunk_size", 5000)
            unique_keys = config.get("unique_keys", [])
            incremental_field = config.get("incremental_field")
            
            # 构建过滤条件
            query = filter_query or {}
            
            # 准备请求
            headers = {}
            if node.get("api_key"):
                headers["X-Sync-API-Key"] = node["api_key"]
            
            # 获取本地数据统计
            local_stats = await self.get_collection_stats(collection_name)
            total_records = local_stats.get("count", 0)
            
            if strategy == "incremental" and incremental_field:
                # 获取远程最新值
                async with httpx.AsyncClient(timeout=30.0) as client:
                    stats_response = await client.post(
                        f"{node['url']}/api/sync/data/stats",
                        headers=headers,
                        json={"collection": collection_name}
                    )
                    if stats_response.status_code == 200:
                        remote_stats = stats_response.json()
                        if remote_stats.get("latest_value"):
                            query[incremental_field] = {"$gt": remote_stats["latest_value"]}
            
            total_inserted = 0
            total_updated = 0
            skip = 0
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                # 分批推送数据
                while True:
                    # 获取本地数据
                    export_result = await self.export_collection_data(
                        collection_name,
                        query,
                        skip,
                        chunk_size
                    )
                    
                    data = export_result.get("data", [])
                    if not data:
                        break
                    
                    # 推送到远程
                    response = await client.post(
                        f"{node['url']}/api/sync/data/import",
                        headers=headers,
                        json={
                            "collection": collection_name,
                            "data": data,
                            "unique_keys": unique_keys,
                            "mode": "upsert"
                        }
                    )
                    
                    if response.status_code != 200:
                        raise Exception(f"推送数据失败: HTTP {response.status_code}")
                    
                    result = response.json()
                    total_inserted += result.get("inserted", 0)
                    total_updated += result.get("updated", 0)
                    
                    # 更新进度
                    await self.update_task_status(task_id, "running", {
                        "total_records": total_records,
                        "transferred": skip + len(data),
                        "inserted": total_inserted,
                        "updated": total_updated,
                        "failed": result.get("failed", 0)
                    })
                    
                    if not export_result.get("has_more"):
                        break
                    
                    skip += chunk_size
            
            # 完成
            await self.update_task_status(task_id, "completed", {
                "total_records": total_records,
                "transferred": skip + len(data) if data else skip,
                "inserted": total_inserted,
                "updated": total_updated,
                "failed": 0
            })
            
            # 更新节点最后同步时间
            await self.nodes_collection.update_one(
                {"node_id": node["node_id"]},
                {"$set": {"last_sync_at": datetime.utcnow()}}
            )
            
        except Exception as e:
            logger.error(f"推送数据失败: {e}", exc_info=True)
            await self.update_task_status(task_id, "failed", error=str(e))
    
    # ==================== 工具方法 ====================
    
    def _serialize_data(self, data: List[Dict]) -> List[Dict]:
        """序列化数据，处理特殊类型"""
        result = []
        for doc in data:
            serialized = {}
            for key, value in doc.items():
                if isinstance(value, datetime):
                    serialized[key] = value.isoformat()
                elif isinstance(value, ObjectId):
                    serialized[key] = str(value)
                else:
                    serialized[key] = value
            result.append(serialized)
        return result
    
    async def get_available_collections(self) -> List[Dict[str, Any]]:
        """获取可同步的集合列表"""
        collections = []
        for name, config in self.COLLECTION_CONFIG.items():
            # 检查集合是否存在
            try:
                coll = self.db.get_collection(name)
                count = await coll.count_documents({})
                collections.append({
                    "name": name,
                    "count": count,
                    "unique_keys": config.get("unique_keys", []),
                    "incremental_field": config.get("incremental_field"),
                    "chunk_size": config.get("chunk_size", 5000)
                })
            except Exception:
                pass
        return collections


# 全局服务实例
_sync_service: Optional[CollectionSyncService] = None


def get_sync_service() -> CollectionSyncService:
    """获取同步服务实例（懒加载）"""
    global _sync_service
    if _sync_service is None:
        from app.core.database import get_mongo_db
        db = get_mongo_db()
        _sync_service = CollectionSyncService(db)
    return _sync_service
