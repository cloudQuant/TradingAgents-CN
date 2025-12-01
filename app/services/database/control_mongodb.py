"""MongoDB 数据库控制类 - 通用的数据写入控制"""
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, date
import pandas as pd
from pymongo import UpdateOne

logger = logging.getLogger(__name__)

# 进度回调类型定义
ProgressCallback = Callable[[int, int, str], None]  # (current, total, message)


class ControlMongodb:
    """
    MongoDB 数据库控制类
    
    根据唯一标识控制写入行为：
    - 唯一标识已存在且数据不同 → 更新
    - 唯一标识已存在且数据相同 → 忽略（MongoDB自动处理）
    - 唯一标识不存在 → 插入
    """
    
    BATCH_SIZE = 1000  # 批量处理大小
    
    def __init__(self, collection, unique_keys: Optional[List[str]] = None, current_user: Optional[Dict[str, Any]] = None):
        """
        初始化
        
        Args:
            collection: MongoDB 集合对象
            unique_keys: 唯一标识字段列表，如 ["基金代码", "股票代码", "季度"]
            current_user: 当前用户信息，用于设置创建人和更新人字段
        """
        self.collection = collection
        self.unique_keys = unique_keys or []
        self.current_user = current_user
        self._indexes_ensured = False  # 标记索引是否已确保创建
    
    def _convert_datetime_fields(self, doc: Dict) -> Dict:
        """统一处理时间字段，转换为 ISO 格式字符串"""
        for key, value in list(doc.items()):
            if isinstance(value, datetime):
                doc[key] = value.isoformat()
            elif isinstance(value, date) and not isinstance(value, datetime):
                # 处理 datetime.date 对象，转换为字符串
                doc[key] = value.isoformat()
            elif pd.isna(value):  # 处理 NaN 值
                doc[key] = None
        return doc
    
    def _build_filter(self, doc: Dict) -> Dict:
        """根据唯一标识构建查询条件"""
        if not self.unique_keys:
            # 没有唯一键时，使用整个文档作为过滤条件（去除更新时间等动态字段）
            return {k: v for k, v in doc.items() if k not in ["更新时间", "scraped_at", "_id"]}
        
        filter_doc = {}
        for key in self.unique_keys:
            value = doc.get(key)
            if value is not None:
                # 处理日期类型：datetime.date 和 datetime.datetime 都转换为字符串
                if isinstance(value, (date, datetime)):
                    filter_doc[key] = value.isoformat() if hasattr(value, 'isoformat') else str(value)
                elif not isinstance(value, (int, float, bool)):
                    filter_doc[key] = str(value)
                else:
                    filter_doc[key] = value
        return filter_doc
    
    def _build_update_operation(self, doc: Dict) -> UpdateOne:
        """构建单个更新操作（兼容旧接口）"""
        current_time = datetime.now().isoformat()
        current_user_name = self.current_user.get("username", "系统") if self.current_user else "系统"
        return self._build_update_operation_optimized(doc, current_time, current_user_name)
    
    def _build_update_operation_optimized(self, doc: Dict, current_time: str, current_user_name: str) -> UpdateOne:
        """构建单个更新操作（优化版：使用预获取的时间）"""
        filter_doc = self._build_filter(doc)
        
        # 添加更新时间和更新人（使用预获取的值）
        doc["更新时间"] = current_time
        if self.current_user:
            doc["更新人"] = current_user_name
        
        if filter_doc:
            # 有有效的过滤条件，使用 upsert
            # 对于 upsert 操作，需要设置创建时间和创建人（仅在插入时）
            set_on_insert = {}
            if self.current_user:
                set_on_insert["创建时间"] = current_time
                set_on_insert["创建人"] = current_user_name
            
            update_doc = {"$set": doc}
            if set_on_insert:
                update_doc["$setOnInsert"] = set_on_insert
                
            return UpdateOne(
                filter_doc,
                update_doc,
                upsert=True
            )
        else:
            # 没有有效过滤条件，直接插入
            # 添加创建时间和创建人
            if self.current_user:
                doc["创建时间"] = current_time
                doc["创建人"] = current_user_name
            
            return UpdateOne(
                doc,
                {"$setOnInsert": doc},
                upsert=True
            )
    
    async def _ensure_indexes(self):
        """
        确保唯一键索引存在（性能优化：避免upsert时的全表扫描）
        
        对于所有数据集合，在保存数据前都会自动检查并创建唯一键索引。
        这样可以显著提升大数据量保存时的性能。
        
        如果存在旧的、不匹配的唯一索引，会自动删除它们以避免冲突。
        """
        if self._indexes_ensured or not self.unique_keys:
            return
        
        try:
            collection_name = self.collection.name
            # 构建复合索引键
            index_keys = [(key, 1) for key in self.unique_keys]
            index_keys_dict = dict(index_keys)
            
            # 生成索引名称（使用下划线连接，避免特殊字符问题）
            index_name = f"idx_{'_'.join(self.unique_keys)}_unique"
            
            # 获取所有现有索引
            existing_indexes = await self.collection.list_indexes().to_list(length=None)
            
            # 检查目标索引是否已存在
            index_exists = any(
                idx.get('name') == index_name or 
                (idx.get('key') and dict(idx.get('key', {})) == index_keys_dict)
                for idx in existing_indexes
            )
            
            # 删除旧的、不匹配的唯一索引（避免冲突）
            # 查找所有唯一索引，如果与当前唯一键不匹配，则删除
            for idx in existing_indexes:
                idx_name = idx.get('name', '')
                idx_key = dict(idx.get('key', {}))
                idx_unique = idx.get('unique', False)
                
                # 跳过 _id 索引
                if idx_name == '_id_':
                    continue
                
                # 如果是唯一索引，且与当前唯一键不匹配，则删除
                if idx_unique:
                    if idx_name != index_name and idx_key != index_keys_dict:
                        try:
                            await self.collection.drop_index(idx_name)
                            logger.info(f"[{collection_name}] 🗑️  已删除旧的唯一索引: {idx_name} (键: {idx_key})")
                        except Exception as e:
                            logger.warning(f"[{collection_name}] 删除旧索引 {idx_name} 时出现错误: {e}")
            
            if not index_exists:
                # 索引不存在，创建索引
                try:
                    await self.collection.create_index(
                        index_keys,
                        unique=True,
                        name=index_name,
                        background=True  # 后台创建，不阻塞其他操作
                    )
                    logger.info(f"[{collection_name}] ✅ 已创建唯一索引: {index_name} on {self.unique_keys}")
                except Exception as e:
                    # 处理并发创建索引的情况（多个实例同时创建）
                    error_msg = str(e).lower()
                    if "already exists" in error_msg or "duplicate" in error_msg or "index already exists" in error_msg:
                        logger.debug(f"[{collection_name}] 索引 {index_name} 已存在（可能由其他实例创建）")
                    else:
                        logger.warning(f"[{collection_name}] 创建索引 {index_name} 时出现错误: {e}")
            else:
                logger.debug(f"[{collection_name}] 索引 {index_name} 已存在，跳过创建")
            
            self._indexes_ensured = True
        except Exception as e:
            logger.warning(f"[{self.collection.name}] 确保索引时出现警告: {e}")
            # 不抛出异常，允许继续执行（即使索引创建失败，也不应该阻止数据保存）
    
    async def _execute_batch(self, ops: List[UpdateOne]) -> Dict[str, int]:
        """执行一批操作"""
        if not ops:
            return {"upserted": 0, "matched": 0, "modified": 0}
        
        result = await self.collection.bulk_write(ops, ordered=False)
        return {
            "upserted": result.upserted_count or 0,
            "matched": result.matched_count or 0,
            "modified": result.modified_count or 0,
        }
    
    async def save_dataframe_to_collection(
        self, 
        df: pd.DataFrame, 
        extra_fields: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[ProgressCallback] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        将 DataFrame 保存到 MongoDB 集合
        
        Args:
            df: 要保存的数据
            extra_fields: 额外添加到每条记录的字段，如 {"数据源": "akshare"}
            progress_callback: 进度回调函数，格式为 (current, total, message)
            **kwargs: 其他参数
            
        Returns:
            包含操作结果的字典
        """
        collection_name = self.collection.name
        logger.info(f"[{collection_name}] 开始保存 {len(df)} 条数据, 唯一键: {self.unique_keys}")
        
        # 性能优化：确保唯一键索引存在（避免upsert时的全表扫描）
        await self._ensure_indexes()
        
        if df is None or df.empty:
            logger.warning(f"[{collection_name}] 数据为空，跳过保存")
            return {
                "success": True,
                "message": "No data to save",
                "inserted": 0,
                "updated": 0,
                "unchanged": 0,
            }
        
        records = df.to_dict("records")
        if not records:
            return {
                "success": True,
                "message": "No records to process",
                "inserted": 0,
                "updated": 0,
                "unchanged": 0,
            }
        
        # 统计结果
        total_upserted = 0
        total_matched = 0
        total_modified = 0
        
        # 性能优化：批量处理前获取一次当前时间，所有记录共用
        current_time = datetime.now().isoformat()
        current_user_name = self.current_user.get("username", "系统") if self.current_user else "系统"
        
        # 分批处理
        ops = []
        batch_count = 0
        total_records = len(records)
        processed_records = 0
        
        # 性能优化：批量转换时间字段（预先处理所有记录）
        # 使用列表推导式批量处理，减少循环开销
        processed_docs = []
        for record in records:
            doc = dict(record)
            
            # 批量转换时间字段（优化：减少函数调用开销）
            for key, value in list(doc.items()):
                if isinstance(value, datetime):
                    doc[key] = value.isoformat()
                elif isinstance(value, date) and not isinstance(value, datetime):
                    doc[key] = value.isoformat()
                elif pd.isna(value):
                    doc[key] = None
            
            # 添加额外字段
            if extra_fields:
                doc.update(extra_fields)
            
            processed_docs.append(doc)
        
        # 批量构建更新操作（优化：减少函数调用开销）
        for doc in processed_docs:
            ops.append(self._build_update_operation_optimized(doc, current_time, current_user_name))
            
            # 达到批量大小时执行
            if len(ops) >= self.BATCH_SIZE:
                batch_count += 1
                # 优化：对于大数据量，使用 INFO 级别日志，但减少日志输出频率
                if batch_count % 5 == 1 or total_records < 10000:  # 每5批或小数据量时输出日志
                    logger.info(f"[{collection_name}] 执行第 {batch_count} 批，共 {len(ops)} 条，总进度: {processed_records + len(ops)}/{total_records}")
                
                result = await self._execute_batch(ops)
                total_upserted += result["upserted"]
                total_matched += result["matched"]
                total_modified += result["modified"]
                processed_records += len(ops)
                ops = []  # 清空当前批次
                
                # 调用进度回调（优化：减少回调频率，只在每批完成后调用）
                if progress_callback:
                    try:
                        progress_callback(
                            processed_records, 
                            total_records, 
                            f"已保存 {processed_records}/{total_records} 条数据"
                        )
                    except Exception as e:
                        logger.debug(f"进度回调失败: {e}")
        
        # 处理剩余的操作
        if ops:
            batch_count += 1
            logger.debug(f"[{collection_name}] 执行第 {batch_count} 批（最后一批），共 {len(ops)} 条")
            
            result = await self._execute_batch(ops)
            total_upserted += result["upserted"]
            total_matched += result["matched"]
            total_modified += result["modified"]
            processed_records += len(ops)
            
            # 调用进度回调
            if progress_callback:
                try:
                    progress_callback(
                        processed_records, 
                        total_records, 
                        f"已保存 {processed_records}/{total_records} 条数据"
                    )
                except Exception as e:
                    logger.debug(f"进度回调失败: {e}")
        
        # 计算结果
        total_processed = total_upserted + total_matched
        unchanged = total_matched - total_modified
        
        logger.info(
            f"[{collection_name}] 保存完成: "
            f"新增={total_upserted}, 更新={total_modified}, "
            f"未变化={unchanged}, 总处理={total_processed}"
        )
        
        return {
            "success": True,
            "message": "Data saved successfully",
            "inserted": total_upserted,
            "updated": total_modified,
            "unchanged": unchanged,
            "total_processed": total_processed,
        }