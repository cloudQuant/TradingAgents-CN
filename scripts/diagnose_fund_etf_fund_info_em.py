#!/usr/bin/env python3
"""
诊断 fund_etf_fund_info_em 数据集合的问题
分析为什么批量下载显示成功1300多个，但实际只有300多个基金
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_mongo_db, init_database, close_database
from app.services.data_sources.funds.providers.fund_etf_fund_info_em_provider import FundEtfFundInfoEmProvider
import pandas as pd


async def diagnose():
    """诊断数据问题"""
    # 初始化数据库
    await init_database()
    
    try:
        db = get_mongo_db()
        
        # 1. 检查源集合 fund_etf_fund_daily_em 中的基金代码数量
        source_collection = db.get_collection("fund_etf_fund_daily_em")
        source_codes = await source_collection.distinct("基金代码")
        print(f"📊 源集合 fund_etf_fund_daily_em 中的基金代码数量: {len(source_codes)}")
        
        # 2. 检查目标集合 fund_etf_fund_info_em 中的基金代码数量
        target_collection = db.get_collection("fund_etf_fund_info_em")
        target_codes = await target_collection.distinct("基金代码")
        print(f"📊 目标集合 fund_etf_fund_info_em 中的基金代码数量: {len(target_codes)}")
        
        # 3. 找出源集合中有但目标集合中没有的基金代码
        missing_codes = set(source_codes) - set(target_codes)
        print(f"❌ 源集合中有但目标集合中没有的基金代码数量: {len(missing_codes)}")
        
        if missing_codes:
            print(f"\n前10个缺失的基金代码: {list(missing_codes)[:10]}")
            
            # 4. 测试其中一个缺失的基金代码，看看能否获取数据
            test_code = list(missing_codes)[0]
            print(f"\n🔍 测试基金代码: {test_code}")
            
            provider = FundEtfFundInfoEmProvider()
            try:
                df = provider.fetch_data(fund_code=test_code)
                if df is not None and not df.empty:
                    print(f"✅ 成功获取数据，共 {len(df)} 条记录")
                    print(f"   数据列: {list(df.columns)}")
                    print(f"   是否有'基金代码'列: {'基金代码' in df.columns}")
                    if '基金代码' in df.columns:
                        unique_codes = df['基金代码'].unique()
                        print(f"   数据中的基金代码: {unique_codes[:5]}...")
                        print(f"   基金代码是否与参数一致: {test_code in unique_codes}")
                else:
                    print(f"❌ 获取的数据为空")
            except Exception as e:
                print(f"❌ 获取数据失败: {e}")
        
        # 5. 检查目标集合中的数据统计
        total_docs = await target_collection.count_documents({})
        print(f"\n📊 目标集合总文档数: {total_docs}")
        
        # 6. 检查是否有基金代码为空或异常的数据
        empty_code_count = await target_collection.count_documents({"基金代码": {"$in": [None, "", "nan"]}})
        print(f"⚠️  基金代码为空或异常的文档数: {empty_code_count}")
        
        # 7. 检查每个基金代码的数据条数分布
        pipeline = [
            {"$group": {
                "_id": "$基金代码",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        top_funds = await target_collection.aggregate(pipeline).to_list(None)
        print(f"\n📊 数据条数最多的前10个基金:")
        for fund in top_funds:
            print(f"   {fund['_id']}: {fund['count']} 条")
        
        # 8. 检查是否有重复的基金代码+净值日期组合
        pipeline = [
            {"$group": {
                "_id": {"基金代码": "$基金代码", "净值日期": "$净值日期"},
                "count": {"$sum": 1}
            }},
            {"$match": {"count": {"$gt": 1}}},
            {"$limit": 10}
        ]
        duplicates = await target_collection.aggregate(pipeline).to_list(None)
        if duplicates:
            print(f"\n⚠️  发现重复的基金代码+净值日期组合: {len(duplicates)} 个")
            for dup in duplicates[:5]:
                print(f"   {dup['_id']}: {dup['count']} 条重复")
        else:
            print(f"\n✅ 未发现重复的基金代码+净值日期组合")
    
    finally:
        # 关闭数据库连接
        await close_database()


if __name__ == "__main__":
    asyncio.run(diagnose())
