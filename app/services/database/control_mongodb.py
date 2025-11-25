"""MongoDB 数据库控制类 - 通用的数据写入控制"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
from pymongo import UpdateOne

logger = logging.getLogger(__name__)


class ControlMongodb:
    """
    MongoDB 数据库控制类
    
    根据唯一标识控制写入行为：
    - 唯一标识已存在且数据不同 → 更新
    - 唯一标识已存在且数据相同 → 忽略（MongoDB自动处理）
    - 唯一标识不存在 → 插入
    """
    
    BATCH_SIZE = 1000  # 批量处理大小
    
    def __init__(self, collection, unique_keys: Optional[List[str]] = None):
        """
        初始化
        
        Args:
            collection: MongoDB 集合对象
            unique_keys: 唯一标识字段列表，如 ["基金代码", "股票代码", "季度"]
        """
        self.collection = collection
        self.unique_keys = unique_keys or []
    
    def _convert_datetime_fields(self, doc: Dict) -> Dict:
        """统一处理时间字段，转换为 ISO 格式字符串"""
        for key, value in list(doc.items()):
            if isinstance(value, datetime):
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
                filter_doc[key] = str(value) if not isinstance(value, (int, float, bool)) else value
        return filter_doc
    
    def _build_update_operation(self, doc: Dict) -> UpdateOne:
        """构建单个更新操作"""
        filter_doc = self._build_filter(doc)
        
        # 添加更新时间
        doc["更新时间"] = datetime.now().isoformat()
        
        if filter_doc:
            # 有有效的过滤条件，使用 upsert
            return UpdateOne(
                filter_doc,
                {"$set": doc},
                upsert=True
            )
        else:
            # 没有有效过滤条件，直接插入
            return UpdateOne(
                doc,
                {"$setOnInsert": doc},
                upsert=True
            )
    
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
        **kwargs
    ) -> Dict[str, Any]:
        """
        将 DataFrame 保存到 MongoDB 集合
        
        Args:
            df: 要保存的数据
            extra_fields: 额外添加到每条记录的字段，如 {"数据源": "akshare"}
            **kwargs: 其他参数
            
        Returns:
            包含操作结果的字典
        """
        collection_name = self.collection.name
        logger.info(f"[{collection_name}] 开始保存 {len(df)} 条数据, 唯一键: {self.unique_keys}")
        
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
        
        # 分批处理
        ops = []
        batch_count = 0
        
        for record in records:
            doc = dict(record)
            
            # 转换时间字段
            doc = self._convert_datetime_fields(doc)
            
            # 添加额外字段
            if extra_fields:
                doc.update(extra_fields)
            
            # 构建更新操作
            ops.append(self._build_update_operation(doc))
            
            # 达到批量大小时执行
            if len(ops) >= self.BATCH_SIZE:
                batch_count += 1
                logger.debug(f"[{collection_name}] 执行第 {batch_count} 批，共 {len(ops)} 条")
                
                result = await self._execute_batch(ops)
                total_upserted += result["upserted"]
                total_matched += result["matched"]
                total_modified += result["modified"]
                ops = []  # 清空当前批次
        
        # 处理剩余的操作
        if ops:
            batch_count += 1
            logger.debug(f"[{collection_name}] 执行第 {batch_count} 批（最后一批），共 {len(ops)} 条")
            
            result = await self._execute_batch(ops)
            total_upserted += result["upserted"]
            total_matched += result["matched"]
            total_modified += result["modified"]
        
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