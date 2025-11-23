#!/usr/bin/env python3
"""
检查fund_info_index_em集合中是否还有NaN/Infinity值
并显示具体哪些字段和记录有问题
"""
import asyncio
import logging
import sys
import math
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_mongo_db, init_database, close_database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_value(value):
    """检查值是否为无效浮点数"""
    if not isinstance(value, (int, float)):
        return False, None
    if isinstance(value, bool):
        return False, None
    try:
        if math.isnan(value):
            return True, "NaN"
        elif math.isinf(value):
            return True, "Infinity" if value > 0 else "-Infinity"
    except (TypeError, ValueError):
        pass
    return False, None


async def check_collection():
    """检查集合中的无效数据"""
    try:
        db = get_mongo_db()
        collection = db.get_collection('fund_info_index_em')
        
        total = await collection.count_documents({})
        logger.info(f"总记录数: {total}")
        
        if total == 0:
            logger.warning("⚠️ 集合为空")
            return False
        
        # 随机抽查一些记录
        sample_size = min(50, total)
        logger.info(f"抽查 {sample_size} 条记录...")
        
        cursor = collection.aggregate([
            {"$sample": {"size": int(sample_size)}}
        ])
        
        problem_count = 0
        problem_fields = {}
        
        async for doc in cursor:
            fund_code = doc.get('基金代码', 'Unknown')
            has_problem = False
            
            for key, value in doc.items():
                if key == '_id':
                    continue
                    
                is_invalid, invalid_type = check_value(value)
                if is_invalid:
                    has_problem = True
                    if key not in problem_fields:
                        problem_fields[key] = 0
                    problem_fields[key] += 1
                    logger.warning(
                        f"发现问题: 基金代码={fund_code}, 字段={key}, "
                        f"值={value}, 类型={invalid_type}"
                    )
            
            if has_problem:
                problem_count += 1
        
        logger.info("=" * 60)
        logger.info(f"抽查结果:")
        logger.info(f"  - 有问题的记录: {problem_count}/{sample_size}")
        
        if problem_fields:
            logger.info(f"  - 有问题的字段:")
            for field, count in sorted(problem_fields.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"    * {field}: {count} 次")
        else:
            logger.info(f"  ✅ 未发现NaN/Infinity值")
        
        logger.info("=" * 60)
        
        return problem_count > 0
        
    except Exception as e:
        logger.error(f"检查失败: {e}", exc_info=True)
        raise


async def test_akshare_data():
    """测试akshare返回的原始数据是否包含NaN"""
    try:
        import akshare as ak
        import pandas as pd
        
        logger.info("=" * 60)
        logger.info("测试 akshare 返回的原始数据...")
        
        # 获取少量数据测试
        df = ak.fund_info_index_em(symbol="全部", indicator="全部")
        
        logger.info(f"获取到 {len(df)} 条记录")
        
        # 检查每列的NaN/Infinity情况
        problem_cols = {}
        for col in df.columns:
            nan_count = df[col].isna().sum()
            inf_count = 0
            
            if df[col].dtype in ['float64', 'int64']:
                inf_count = ((df[col] == float('inf')) | (df[col] == float('-inf'))).sum()
            
            if nan_count > 0 or inf_count > 0:
                problem_cols[col] = {
                    'nan': nan_count,
                    'inf': inf_count
                }
        
        if problem_cols:
            logger.warning("⚠️ akshare返回的数据包含无效值:")
            for col, counts in problem_cols.items():
                logger.warning(f"  - {col}: NaN={counts['nan']}, Infinity={counts['inf']}")
        else:
            logger.info("✅ akshare返回的数据没有无效值")
        
        logger.info("=" * 60)
        
        return len(problem_cols) > 0
        
    except Exception as e:
        logger.error(f"测试akshare数据失败: {e}", exc_info=True)
        return False


async def main():
    """主函数"""
    try:
        await init_database()
        
        logger.info("=" * 60)
        logger.info("检查数据库中的数据")
        logger.info("=" * 60)
        
        has_db_problem = await check_collection()
        
        # 测试akshare原始数据
        has_akshare_problem = await test_akshare_data()
        
        logger.info("=" * 60)
        logger.info("检查完成")
        if has_db_problem:
            logger.warning("⚠️ 数据库中存在无效值，需要运行修复脚本")
        else:
            logger.info("✅ 数据库数据正常")
            
        if has_akshare_problem:
            logger.warning("⚠️ akshare返回的数据包含无效值，这是数据源的问题")
            logger.info("💡 解决方案: 代码中已添加数据清理逻辑，重启服务器后生效")
        
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
