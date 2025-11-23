#!/usr/bin/env python3
"""
修复 fund_info_index_em 集合中的无效浮点数值（NaN, Infinity等）
这些值无法被序列化为JSON，导致API返回500错误
"""
import asyncio
import logging
import sys
import os
from pathlib import Path
import math

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_mongo_db, init_database, close_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def is_invalid_float(value):
    """检查是否为无效的浮点数"""
    if not isinstance(value, (int, float)):
        return False
    if isinstance(value, bool):  # bool是int的子类，需要排除
        return False
    try:
        return math.isnan(value) or math.isinf(value)
    except (TypeError, ValueError):
        return False


def clean_document(doc):
    """清理文档中的无效浮点数"""
    if not isinstance(doc, dict):
        return doc
    
    cleaned = {}
    for key, value in doc.items():
        if key == '_id':
            cleaned[key] = value
            continue
            
        if is_invalid_float(value):
            cleaned[key] = None
            logger.debug(f"替换无效值: {key}={value} -> None")
        elif isinstance(value, dict):
            cleaned[key] = clean_document(value)
        elif isinstance(value, list):
            cleaned[key] = [clean_document(item) if isinstance(item, dict) else (None if is_invalid_float(item) else item) for item in value]
        else:
            cleaned[key] = value
    
    return cleaned


async def fix_fund_info_index_collection():
    """修复 fund_info_index_em 集合中的无效浮点数"""
    try:
        db = get_mongo_db()
        collection = db.get_collection('fund_info_index_em')
        
        logger.info("开始扫描 fund_info_index_em 集合...")
        
        # 统计信息
        total_count = await collection.count_documents({})
        logger.info(f"总共 {total_count} 条记录")
        
        fixed_count = 0
        batch_size = 500
        skip = 0
        
        while skip < total_count:
            logger.info(f"处理记录 {skip + 1} 到 {min(skip + batch_size, total_count)}...")
            
            # 分批读取
            cursor = collection.find({}).skip(skip).limit(batch_size)
            docs = await cursor.to_list(length=batch_size)
            
            if not docs:
                break
            
            # 批量更新
            from pymongo import UpdateOne
            updates = []
            
            for doc in docs:
                cleaned_doc = clean_document(doc)
                
                # 检查是否有变化
                if cleaned_doc != doc:
                    # 移除_id字段用于更新
                    doc_id = cleaned_doc.pop('_id')
                    updates.append(
                        UpdateOne(
                            {'_id': doc_id},
                            {'$set': cleaned_doc}
                        )
                    )
                    fixed_count += 1
            
            # 执行批量更新
            if updates:
                result = await collection.bulk_write(updates, ordered=False)
                logger.info(f"本批修复了 {len(updates)} 条记录")
            
            skip += batch_size
        
        logger.info(f"✅ 修复完成！总共修复了 {fixed_count} 条记录")
        return fixed_count
        
    except Exception as e:
        logger.error(f"修复失败: {e}", exc_info=True)
        raise


async def main():
    """主函数"""
    try:
        # 初始化数据库连接
        logger.info("初始化数据库连接...")
        await init_database()
        
        logger.info("=" * 60)
        logger.info("开始修复 fund_info_index_em 集合中的无效浮点数")
        logger.info("=" * 60)
        
        fixed_count = await fix_fund_info_index_collection()
        
        logger.info("=" * 60)
        logger.info(f"修复完成！共修复 {fixed_count} 条记录")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # 关闭数据库连接
        logger.info("关闭数据库连接...")
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
