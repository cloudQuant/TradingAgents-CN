"""
基金数据通用服务 V2
只保留通用功能，具体数据集合的操作由各自的service处理
"""
import logging
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
import pandas as pd
import io

logger = logging.getLogger("webapi")


class FundDataService:
    """基金数据通用服务类"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        # 兼容旧版 FundDataService 中使用的集合别名
        self.col_fund_portfolio_hold_em = self.db.funds.fund_portfolio_hold_em
    
    async def import_data_from_file(
        self, 
        collection_name: str, 
        content: bytes, 
        filename: str
    ) -> Dict[str, Any]:
        """
        从文件导入数据到指定集合
        
        Args:
            collection_name: 集合名称
            content: 文件内容（字节）
            filename: 文件名
            
        Returns:
            导入结果
        """
        try:
            collection = self.db.get_collection(collection_name)
            
            if filename.endswith('.csv'):
                # 解析CSV
                df = pd.read_csv(io.BytesIO(content))
            elif filename.endswith(('.xls', '.xlsx')):
                # 解析Excel
                df = pd.read_excel(io.BytesIO(content))
            elif filename.endswith('.json'):
                # 解析JSON
                df = pd.read_json(io.BytesIO(content))
            else:
                raise ValueError(f"不支持的文件格式: {filename}")
            
            if df.empty:
                return {
                    "success": False,
                    "message": "文件中没有数据",
                    "imported": 0
                }
            
            # 转换为字典列表
            records = df.to_dict('records')
            
            # 批量插入
            result = await collection.insert_many(records)
            
            return {
                "success": True,
                "message": f"成功导入 {len(result.inserted_ids)} 条数据",
                "imported": len(result.inserted_ids),
                "total_rows": len(df)
            }
            
        except Exception as e:
            logger.error(f"导入文件失败: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"导入失败: {str(e)}",
                "imported": 0
            }
    
    async def sync_data_from_remote(
        self, 
        collection_name: str, 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从远程数据库同步数据到本地集合
        
        Args:
            collection_name: 集合名称
            config: 远程数据库配置
                {
                    "host": "远程主机",
                    "port": 端口,
                    "database": "数据库名",
                    "collection": "集合名",
                    "username": "用户名（可选）",
                    "password": "密码（可选）"
                }
            
        Returns:
            同步结果
        """
        from motor.motor_asyncio import AsyncIOMotorClient
        
        try:
            # 连接远程数据库
            remote_uri = f"mongodb://"
            if config.get("username") and config.get("password"):
                remote_uri += f"{config['username']}:{config['password']}@"
            remote_uri += f"{config['host']}:{config.get('port', 27017)}"
            
            remote_client = AsyncIOMotorClient(remote_uri)
            remote_db = remote_client[config['database']]
            remote_collection = remote_db[config.get('collection', collection_name)]
            
            # 获取本地集合
            local_collection = self.db.get_collection(collection_name)
            
            # 获取远程数据
            cursor = remote_collection.find({})
            remote_data = await cursor.to_list(length=None)
            
            if not remote_data:
                remote_client.close()
                return {
                    "success": True,
                    "message": "远程数据库中没有数据",
                    "synced": 0
                }
            
            # 清空本地数据
            await local_collection.delete_many({})
            
            # 插入远程数据
            # 移除 _id 字段以避免冲突
            for doc in remote_data:
                if '_id' in doc:
                    del doc['_id']
            
            result = await local_collection.insert_many(remote_data)
            
            # 关闭远程连接
            remote_client.close()
            
            return {
                "success": True,
                "message": f"成功同步 {len(result.inserted_ids)} 条数据",
                "synced": len(result.inserted_ids),
                "total_remote": len(remote_data)
            }
            
        except Exception as e:
            logger.error(f"远程同步失败: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"同步失败: {str(e)}",
                "synced": 0
            }
    
    async def export_data_to_file(
        self, 
        collection_name: str, 
        file_format: str = 'csv',
        filters: Dict = None
    ) -> bytes:
        """
        导出集合数据到文件
        
        Args:
            collection_name: 集合名称
            file_format: 文件格式 ('csv', 'excel', 'json')
            filters: 查询过滤条件
            
        Returns:
            文件内容（字节）
        """
        try:
            collection = self.db.get_collection(collection_name)
            
            # 查询数据
            query = filters or {}
            cursor = collection.find(query)
            data = await cursor.to_list(length=None)
            
            if not data:
                raise ValueError("没有数据可导出")
            
            # 转换为DataFrame
            df = pd.DataFrame(data)
            
            # 移除 _id 字段
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            
            # 根据格式导出
            if file_format == 'csv':
                return df.to_csv(index=False).encode('utf-8-sig')
            elif file_format == 'excel':
                output = io.BytesIO()
                df.to_excel(output, index=False)
                return output.getvalue()
            elif file_format == 'json':
                return df.to_json(orient='records', force_ascii=False).encode('utf-8')
            else:
                raise ValueError(f"不支持的文件格式: {file_format}")
                
        except Exception as e:
            logger.error(f"导出文件失败: {e}", exc_info=True)
            raise
    
    async def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        """
        获取集合基本信息
        
        Args:
            collection_name: 集合名称
            
        Returns:
            集合信息
        """
        try:
            collection = self.db.get_collection(collection_name)
            
            total_count = await collection.count_documents({})
            
            # 获取最新和最旧的记录（如果有scraped_at字段）
            latest = await collection.find_one(sort=[("scraped_at", -1)])
            oldest = await collection.find_one(sort=[("scraped_at", 1)])
            
            # 获取示例文档（用于了解字段结构）
            sample = await collection.find_one()
            
            return {
                "collection_name": collection_name,
                "total_count": total_count,
                "last_updated": latest.get("scraped_at") if latest and "scraped_at" in latest else None,
                "oldest_date": oldest.get("scraped_at") if oldest and "scraped_at" in oldest else None,
                "fields": list(sample.keys()) if sample else []
            }
            
        except Exception as e:
            logger.error(f"获取集合信息失败: {e}", exc_info=True)
            raise

    async def clear_fund_data(self, collection_name: str) -> int:
        """
        清空指定基金数据集合
        
        Args:
            collection_name: 集合名称（如 fund_name_em）
            
        Returns:
            删除的记录数
        """
        try:
            # 使用 get_collection 访问集合，与 get_fund_collection_data API 保持一致
            collection = self.db.get_collection(collection_name)
            result = await collection.delete_many({})
            logger.info(f"成功清空集合 {collection_name}: {result.deleted_count} 条记录")
            return result.deleted_count
        except Exception as e:
            logger.error(f"清空集合 {collection_name} 失败: {e}", exc_info=True)
            raise
