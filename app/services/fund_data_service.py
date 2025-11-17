"""
基金数据服务
负责从akshare获取基金数据并存储到MongoDB
"""
import logging
from typing import Dict, Any, List, Optional
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
    
    async def save_fund_name_em_data(self, df: pd.DataFrame) -> int:
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
            ops = []
            for idx, row in df.iterrows():
                doc = row.to_dict()
                
                # 添加元数据
                fund_code = str(doc.get('基金代码', ''))
                doc['code'] = fund_code
                doc['source'] = 'akshare'
                doc['endpoint'] = 'fund_name_em'
                
                # 使用基金代码作为唯一标识
                ops.append(
                    UpdateOne(
                        {'code': fund_code, 'endpoint': 'fund_name_em'},
                        {'$set': doc},
                        upsert=True
                    )
                )
            
            if ops:
                result = await self.col_fund_name_em.bulk_write(ops, ordered=False)
                saved_count = (
                    (result.upserted_count or 0) + 
                    (result.modified_count or 0) + 
                    (result.matched_count or 0)
                )
                logger.info(f"成功保存 {saved_count} 条基金基本信息数据")
                return saved_count
            else:
                logger.warning("没有生成任何保存操作")
                return 0
                
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
    
    async def save_fund_basic_info_data(self, df: pd.DataFrame) -> int:
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
            ops = []
            for idx, row in df.iterrows():
                doc = row.to_dict()
                
                # 添加元数据
                fund_code = str(doc.get('基金代码', ''))
                doc['code'] = fund_code
                doc['source'] = 'akshare'
                doc['endpoint'] = 'fund_name_em'
                
                # 使用基金代码作为唯一标识
                ops.append(
                    UpdateOne(
                        {'code': fund_code, 'endpoint': 'fund_name_em'},
                        {'$set': doc},
                        upsert=True
                    )
                )
            
            if ops:
                result = await self.col_fund_basic_info.bulk_write(ops, ordered=False)
                saved_count = (
                    (result.upserted_count or 0) + 
                    (result.modified_count or 0) + 
                    (result.matched_count or 0)
                )
                logger.info(f"成功保存 {saved_count} 条基金基本信息数据到fund_basic_info集合")
                return saved_count
            else:
                logger.warning("没有生成任何保存操作")
                return 0
                
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
