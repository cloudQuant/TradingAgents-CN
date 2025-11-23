#!/usr/bin/env python3
"""
基金申购状态功能快速验证脚本
用于验证基本功能是否正常工作
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService
import pandas as pd


async def verify_basic_functionality():
    """验证基本功能"""
    print("=" * 60)
    print("基金申购状态功能验证")
    print("=" * 60)
    
    # 1. 获取数据库连接
    print("\n1. 检查数据库连接...")
    try:
        db = get_mongo_db()
        service = FundDataService(db)
        print("   ✅ 数据库连接成功")
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        return False
    
    # 2. 检查集合是否存在
    print("\n2. 检查fund_purchase_status集合...")
    try:
        collection = db.get_collection("fund_purchase_status")
        count = await collection.count_documents({})
        print(f"   ✅ 集合存在，当前记录数: {count}")
    except Exception as e:
        print(f"   ❌ 集合检查失败: {e}")
        return False
    
    # 3. 测试保存数据功能
    print("\n3. 测试保存数据功能...")
    try:
        test_data = pd.DataFrame([
            {
                '序号': '1',
                '基金代码': 'TEST001',
                '基金简称': '测试基金A',
                '基金类型': '混合型',
                '最新净值/万份收益': 1.234,
                '最新净值/万份收益-报告时间': '2024-01-01',
                '申购状态': '开放申购',
                '赎回状态': '开放赎回',
                '下一开放日': '2024-01-02',
                '购买起点': 10.0,
                '日累计限定金额': 100000000.0,
                '手续费': 0.15
            }
        ])
        
        saved = await service.save_fund_purchase_status_data(test_data)
        print(f"   ✅ 数据保存成功，保存了 {saved} 条记录")
    except Exception as e:
        print(f"   ❌ 保存数据失败: {e}")
        return False
    
    # 4. 测试统计功能
    print("\n4. 测试统计功能...")
    try:
        stats = await service.get_fund_purchase_status_stats()
        print(f"   ✅ 统计信息获取成功")
        print(f"      - 总记录数: {stats.get('total_count', 0)}")
        
        if stats.get('type_stats'):
            print(f"      - 基金类型数: {len(stats['type_stats'])}")
            for item in stats['type_stats'][:3]:
                print(f"        • {item.get('type', '未知')}: {item.get('count', 0)}条")
        
        if stats.get('purchase_status_stats'):
            print(f"      - 申购状态:")
            for item in stats['purchase_status_stats']:
                print(f"        • {item.get('status', '未知')}: {item.get('count', 0)}条")
        
        if stats.get('redeem_status_stats'):
            print(f"      - 赎回状态:")
            for item in stats['redeem_status_stats']:
                print(f"        • {item.get('status', '未知')}: {item.get('count', 0)}条")
                
    except Exception as e:
        print(f"   ❌ 获取统计信息失败: {e}")
        return False
    
    # 5. 清理测试数据
    print("\n5. 清理测试数据...")
    try:
        await collection.delete_many({'基金代码': 'TEST001'})
        print("   ✅ 测试数据清理成功")
    except Exception as e:
        print(f"   ⚠️  清理测试数据失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 所有验证通过！")
    print("=" * 60)
    print("\n下一步：")
    print("1. 启动后端服务: python main.py")
    print("2. 启动前端服务: cd frontend && npm run dev")
    print("3. 访问: http://localhost:5173/funds/collections/fund_purchase_status")
    print("4. 点击'更新数据'按钮，从东方财富网获取真实数据")
    
    return True


async def main():
    """主函数"""
    try:
        success = await verify_basic_functionality()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
