"""
指数数据服务
提供数据导入、导出、同步等功能
"""
import io
import json
import logging
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class IndexDataService:
    """指数数据服务"""
    
    def __init__(self, db):
        """
        初始化服务
        
        Args:
            db: MongoDB 数据库实例
        """
        self.db = db
    
    async def export_data_to_file(
        self,
        collection_name: str,
        file_format: str = "xlsx",
        filters: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        导出集合数据到文件
        
        Args:
            collection_name: 集合名称
            file_format: 文件格式 (csv, xlsx, json)
            filters: 过滤条件
            
        Returns:
            文件字节内容
        """
        collection = self.db.get_collection(collection_name)
        query = filters or {}
        
        cursor = collection.find(query)
        items = []
        async for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            items.append(doc)
        
        if not items:
            # 返回空文件
            if file_format == "json":
                return b"[]"
            elif file_format == "csv":
                return b""
            else:
                df = pd.DataFrame()
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False)
                return buffer.getvalue()
        
        df = pd.DataFrame(items)
        
        if file_format == "json":
            return df.to_json(orient="records", force_ascii=False).encode("utf-8")
        elif file_format == "csv":
            return df.to_csv(index=False).encode("utf-8")
        else:  # xlsx
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            return buffer.getvalue()
    
    async def import_data_from_file(
        self,
        collection_name: str,
        content: bytes,
        filename: str,
    ) -> Dict[str, Any]:
        """
        从文件导入数据
        
        Args:
            collection_name: 集合名称
            content: 文件内容
            filename: 文件名
            
        Returns:
            导入结果
        """
        # 根据文件扩展名解析数据
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith(".json"):
            df = pd.read_json(io.BytesIO(content))
        else:
            raise ValueError(f"不支持的文件格式: {filename}")
        
        if df.empty:
            return {"success": True, "inserted": 0, "message": "文件为空"}
        
        # 转换为字典列表
        records = df.to_dict(orient="records")
        
        # 插入数据
        collection = self.db.get_collection(collection_name)
        result = await collection.insert_many(records)
        
        return {
            "success": True,
            "inserted": len(result.inserted_ids),
            "message": f"成功导入 {len(result.inserted_ids)} 条数据"
        }
    
    async def sync_data_from_remote(
        self,
        collection_name: str,
        sync_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        从远程 MongoDB 同步数据
        
        Args:
            collection_name: 集合名称
            sync_config: 同步配置
            
        Returns:
            同步结果
        """
        from motor.motor_asyncio import AsyncIOMotorClient
        
        remote_host = sync_config.get("remote_host")
        remote_collection = sync_config.get("remote_collection", collection_name)
        batch_size = sync_config.get("batch_size", 5000)
        remote_username = sync_config.get("remote_username")
        remote_password = sync_config.get("remote_password")
        remote_auth_source = sync_config.get("remote_auth_source", "admin")
        
        if not remote_host:
            raise ValueError("远程主机地址不能为空")
        
        # 构建连接字符串
        if remote_username and remote_password:
            connection_string = f"mongodb://{remote_username}:{remote_password}@{remote_host}/?authSource={remote_auth_source}"
        else:
            connection_string = f"mongodb://{remote_host}/"
        
        # 连接远程数据库
        remote_client = AsyncIOMotorClient(connection_string)
        remote_db = remote_client.get_default_database()
        remote_col = remote_db.get_collection(remote_collection)
        
        # 获取本地集合
        local_col = self.db.get_collection(collection_name)
        
        # 分批同步
        total_synced = 0
        cursor = remote_col.find({})
        
        batch = []
        async for doc in cursor:
            if "_id" in doc:
                del doc["_id"]
            batch.append(doc)
            
            if len(batch) >= batch_size:
                if batch:
                    await local_col.insert_many(batch)
                    total_synced += len(batch)
                    batch = []
        
        # 处理剩余数据
        if batch:
            await local_col.insert_many(batch)
            total_synced += len(batch)
        
        remote_client.close()
        
        return {
            "success": True,
            "synced": total_synced,
            "message": f"成功同步 {total_synced} 条数据"
        }
    
    async def clear_index_data(self, collection_name: str) -> int:
        """
        清空指数集合数据
        
        Args:
            collection_name: 集合名称
            
        Returns:
            删除的记录数
        """
        collection = self.db.get_collection(collection_name)
        result = await collection.delete_many({})
        return result.deleted_count
