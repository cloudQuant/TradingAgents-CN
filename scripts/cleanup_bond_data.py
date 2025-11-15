#!/usr/bin/env python3
"""
清理旧债券数据的脚本
根据新的数据表结构，清理所有旧的债券数据，以便重新同步
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import get_mongo_db


async def cleanup_bond_data():
    """清理所有债券相关数据表"""
    db = get_mongo_db()
    
    # 要清理的集合列表
    collections_to_clean = [
        "bond_basic_info",
        "bond_daily",
        "yield_curve_daily",
        "bond_events",
        "bond_spot_quotes",
        "bond_indices_daily",
        "bond_cb_profiles",
        "bond_buybacks",
        "bond_issues",
        "bond_cb_adjustments",
        "bond_cb_redeems",
        "bond_cb_summary",
        "bond_cb_valuation_daily",
        "bond_cb_comparison",
        "bond_spot_quote_detail",
        "bond_spot_deals",
        "bond_deal_summary",
        "bond_cash_summary",
        "bond_nafmii_debts",
        "bond_info_cm",
        "yield_curve_map",
        "bond_buybacks_hist",
        "bond_cb_list_jsl",
        "bond_cov_list",
    ]
    
    print("=" * 60)
    print("债券数据清理工具")
    print("=" * 60)
    print(f"\n将清理以下 {len(collections_to_clean)} 个集合:")
    for i, col_name in enumerate(collections_to_clean, 1):
        print(f"  {i}. {col_name}")
    
    print("\n⚠️  警告: 此操作将删除所有债券相关数据！")
    print("   数据可以重新从 AKShare 同步获取。")
    
    confirm = input("\n是否确认删除？(输入 'YES' 确认): ")
    if confirm != "YES":
        print("操作已取消。")
        return
    
    print("\n开始清理...")
    
    total_deleted = 0
    for col_name in collections_to_clean:
        try:
            collection = db.get_collection(col_name)
            count = await collection.count_documents({})
            if count > 0:
                result = await collection.delete_many({})
                deleted = result.deleted_count
                total_deleted += deleted
                print(f"  ✅ {col_name}: 删除了 {deleted} 条记录")
            else:
                print(f"  ⚪ {col_name}: 集合为空，跳过")
        except Exception as e:
            print(f"  ❌ {col_name}: 清理失败 - {e}")
    
    print("\n" + "=" * 60)
    print(f"清理完成！总共删除了 {total_deleted} 条记录。")
    print("=" * 60)
    print("\n💡 提示: 现在可以运行同步任务重新获取数据:")
    print("   - 债券基础信息同步")
    print("   - 债券收益率曲线同步")
    print("   - 债券历史数据同步")
    print("   - 中债信息详情同步")
    print("")


if __name__ == "__main__":
    asyncio.run(cleanup_bond_data())

