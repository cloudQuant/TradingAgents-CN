#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理债券持仓数据表中的重复英文字段
将旧的英文字段删除，保留中文字段
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import sys

async def cleanup_bond_hold_fields():
    """清理债券持仓字段"""
    print("=" * 80)
    print("清理债券持仓数据表字段")
    print("=" * 80)
    print()
    
    # 连接数据库
    print("📡 连接数据库...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    collection = db['fund_portfolio_bond_hold_em']
    
    # 统计当前数据
    total_count = await collection.count_documents({})
    print(f"📊 当前数据总数: {total_count} 条")
    
    if total_count == 0:
        print("✅ 数据表为空，无需清理")
        return
    
    # 检查是否有旧字段
    sample = await collection.find_one({})
    if sample:
        print(f"\n📋 示例数据字段:")
        for i, key in enumerate(sample.keys(), 1):
            print(f"  {i}. {key}")
    
    # 询问是否继续
    print()
    print("⚠️  即将删除以下重复的英文字段:")
    print("  - code (与 '基金代码' 重复)")
    print("  - bond_code (与 '债券代码' 重复)")
    print("  - quarter (与 '季度' 重复)")
    print("  - source (改为 '数据源')")
    print("  - endpoint (改为 '接口名称')")
    print("  - updated_at (改为 '更新时间')")
    print("  - 序号 (不需要)")
    print()
    
    response = input("是否继续清理？(yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ 取消清理")
        return
    
    print()
    print("🧹 开始清理...")
    
    # 删除重复的英文字段
    result = await collection.update_many(
        {},
        {'$unset': {
            'code': '',
            'bond_code': '',
            'quarter': '',
            'source': '',
            'endpoint': '',
            'updated_at': '',
            '序号': ''
        }}
    )
    
    print(f"✅ 清理完成！")
    print(f"   匹配文档数: {result.matched_count}")
    print(f"   修改文档数: {result.modified_count}")
    
    # 显示清理后的示例
    sample_after = await collection.find_one({})
    if sample_after:
        print(f"\n📋 清理后示例数据字段:")
        for i, key in enumerate(sample_after.keys(), 1):
            print(f"  {i}. {key}")
    
    # 统计信息
    print()
    print("=" * 80)
    print("📊 数据统计:")
    unique_funds = len(await collection.distinct('基金代码'))
    unique_bonds = len(await collection.distinct('债券代码'))
    unique_quarters = len(await collection.distinct('季度'))
    
    print(f"  总记录数: {total_count}")
    print(f"  基金数量: {unique_funds}")
    print(f"  债券数量: {unique_bonds}")
    print(f"  季度数量: {unique_quarters}")
    print("=" * 80)
    
    client.close()

async def show_statistics():
    """仅显示统计信息，不做任何修改"""
    print("=" * 80)
    print("债券持仓数据表统计信息")
    print("=" * 80)
    print()
    
    # 连接数据库
    print("📡 连接数据库...")
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    collection = db['fund_portfolio_bond_hold_em']
    
    # 统计
    total_count = await collection.count_documents({})
    print(f"📊 总记录数: {total_count}")
    
    if total_count > 0:
        # 显示示例
        sample = await collection.find_one({})
        print(f"\n📋 数据字段:")
        for i, key in enumerate(sample.keys(), 1):
            marker = ""
            if key in ['code', 'bond_code', 'quarter', 'source', 'endpoint', 'updated_at', '序号']:
                marker = " ❌ (需要清理)"
            elif key in ['基金代码', '债券代码', '季度', '数据源', '接口名称', '更新时间']:
                marker = " ✅ (正确)"
            print(f"  {i}. {key}{marker}")
        
        # 检查是否有旧字段
        has_old_fields = any(key in sample for key in ['code', 'bond_code', 'quarter', 'source', 'endpoint', 'updated_at', '序号'])
        
        print()
        if has_old_fields:
            print("⚠️  检测到旧的英文字段，建议运行清理脚本")
            print("   运行: python cleanup_bond_hold_fields.py --cleanup")
        else:
            print("✅ 字段结构正确，无需清理")
        
        # 详细统计
        unique_funds = len(await collection.distinct('基金代码'))
        unique_bonds = len(await collection.distinct('债券代码'))
        unique_quarters = len(await collection.distinct('季度'))
        
        print()
        print("=" * 80)
        print("详细统计:")
        print(f"  基金数量: {unique_funds}")
        print(f"  债券数量: {unique_bonds}")
        print(f"  季度数量: {unique_quarters}")
        print("=" * 80)
    
    client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--cleanup':
        asyncio.run(cleanup_bond_hold_fields())
    else:
        asyncio.run(show_statistics())
