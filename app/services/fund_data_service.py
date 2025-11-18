"""
基金数据服务
负责从akshare获取基金数据并存储到MongoDB
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
import asyncio

logger = logging.getLogger("webapi")


class FundDataService:
    """基金数据服务类"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.col_fund_name_em = db.get_collection("fund_name_em")
        self.col_fund_basic_info = db.get_collection("fund_basic_info")
    
    async def save_fund_name_em_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金基本信息数据到MongoDB
        
        Args:
            df: 包含基金基本信息的DataFrame
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金基本信息数据需要保存")
            return 0
        
        try:
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金数据...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_name_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'endpoint': 'fund_name_em'},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_name_em.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据 ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入完成: 总计保存 {total_saved}/{total_count} 条基金数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金基本信息数据失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_name_em_data(self) -> int:
        """
        清空基金基本信息数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_name_em.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空 {deleted_count} 条基金基本信息数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空基金基本信息数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_name_em_stats(self) -> Dict[str, Any]:
        """
        获取基金基本信息统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_name_em.count_documents({})
            
            # 按基金类型统计
            pipeline = [
                {
                    '$group': {
                        '_id': '$基金类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats = []
            async for doc in self.col_fund_name_em.aggregate(pipeline):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'type_stats': type_stats
            }
        except Exception as e:
            logger.error(f"获取基金基本信息统计失败: {e}", exc_info=True)
            raise
    
    async def save_fund_basic_info_data(self, df: pd.DataFrame, progress_callback=None) -> int:
        """
        保存基金基本信息数据到fund_basic_info集合
        使用相同的fund_name_em数据源
        
        Args:
            df: 包含基金基本信息的DataFrame
            
        Returns:
            保存的记录数
        """
        if df is None or df.empty:
            logger.warning("没有基金基本信息数据需要保存")
            return 0
        
        try:
            total_count = len(df)
            logger.info(f"📊 开始处理 {total_count} 条基金数据到fund_basic_info集合...")
            
            # 分批处理，每批500条
            batch_size = 500
            total_saved = 0
            total_batches = (total_count + batch_size - 1) // batch_size
            
            logger.info(f"📦 将分 {total_batches} 批次处理，每批 {batch_size} 条")
            
            for batch_idx in range(total_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, total_count)
                batch_df = df.iloc[start_idx:end_idx]
                
                logger.info(f"📝 处理第 {batch_idx + 1}/{total_batches} 批，记录范围: {start_idx + 1}-{end_idx}")
                
                # 构建批量操作
                ops = []
                for idx, row in batch_df.iterrows():
                    doc = row.to_dict()
                    
                    # 添加元数据
                    fund_code = str(doc.get('基金代码', ''))
                    doc['code'] = fund_code
                    doc['source'] = 'akshare'
                    doc['endpoint'] = 'fund_name_em'
                    doc['updated_at'] = datetime.now().isoformat()
                    
                    # 使用基金代码作为唯一标识
                    ops.append(
                        UpdateOne(
                            {'code': fund_code, 'endpoint': 'fund_name_em'},
                            {'$set': doc},
                            upsert=True
                        )
                    )
                
                # 执行批量写入
                if ops:
                    result = await self.col_fund_basic_info.bulk_write(ops, ordered=False)
                    batch_saved = (result.upserted_count or 0) + (result.matched_count or 0)
                    total_saved += batch_saved
                    
                    logger.info(
                        f"✅ 第 {batch_idx + 1}/{total_batches} 批写入fund_basic_info完成: "
                        f"新增={result.upserted_count}, 更新={result.matched_count}, "
                        f"本批保存={batch_saved}, 累计={total_saved}/{total_count}"
                    )
                    
                    # 调用进度回调（如果提供）
                    if progress_callback:
                        progress = int((end_idx / total_count) * 100)
                        progress_callback(
                            current=end_idx,
                            total=total_count,
                            percentage=progress,
                            message=f"已保存 {end_idx}/{total_count} 条数据到fund_basic_info ({progress}%)"
                        )
            
            logger.info(f"🎉 全部数据写入fund_basic_info完成: 总计保存 {total_saved}/{total_count} 条基金数据")
            return total_saved
                
        except Exception as e:
            logger.error(f"保存基金基本信息数据到fund_basic_info失败: {e}", exc_info=True)
            raise
    
    async def clear_fund_basic_info_data(self) -> int:
        """
        清空fund_basic_info基金数据
        
        Returns:
            删除的记录数
        """
        try:
            result = await self.col_fund_basic_info.delete_many({})
            deleted_count = result.deleted_count
            logger.info(f"成功清空fund_basic_info {deleted_count} 条数据")
            return deleted_count
        except Exception as e:
            logger.error(f"清空fund_basic_info数据失败: {e}", exc_info=True)
            raise
    
    async def get_fund_basic_info_stats(self) -> Dict[str, Any]:
        """
        获取fund_basic_info集合统计
        
        Returns:
            统计信息字典
        """
        try:
            total_count = await self.col_fund_basic_info.count_documents({})
            
            # 按基金类型统计
            pipeline = [
                {
                    '$group': {
                        '_id': '$基金类型',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                }
            ]
            
            type_stats = []
            async for doc in self.col_fund_basic_info.aggregate(pipeline):
                type_stats.append({
                    'type': doc['_id'],
                    'count': doc['count']
                })
            
            return {
                'total_count': total_count,
                'type_stats': type_stats
            }
        except Exception as e:
            logger.error(f"获取fund_basic_info统计失败: {e}", exc_info=True)
            raise
