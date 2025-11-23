#!/usr/bin/env python3
"""
测试datetime.date编码问题的修复
验证日期字段能正确转换并保存到MongoDB
"""
import asyncio
import sys
import os
from datetime import date, datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService


async def test_datetime_conversion():
    """测试日期类型转换"""
    print("=" * 60)
    print("测试datetime.date编码修复")
    print("=" * 60)
    
    # 1. 获取数据库连接
    print("\n1. 连接数据库...")
    try:
        db = get_mongo_db()
        service = FundDataService(db)
        print("   ✅ 数据库连接成功")
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        return False
    
    # 2. 创建包含datetime.date对象的测试数据
    print("\n2. 创建测试数据（包含datetime.date对象）...")
    try:
        test_data = pd.DataFrame([
            {
                '序号': '9999',
                '基金代码': 'TEST999',
                '基金简称': '测试基金-日期修复',
                '基金类型': '混合型',
                '最新净值/万份收益': 1.234,
                '最新净值/万份收益-报告时间': date(2024, 11, 22),  # datetime.date对象
                '申购状态': '开放申购',
                '赎回状态': '开放赎回',
                '下一开放日': date(2025, 12, 8),  # datetime.date对象 - 这是导致错误的字段
                '购买起点': 10.0,
                '日累计限定金额': 100000000.0,
                '手续费': 0.15
            },
            {
                '序号': '10000',
                '基金代码': 'TEST1000',
                '基金简称': '测试基金-None日期',
                '基金类型': '债券型',
                '最新净值/万份收益': 2.345,
                '最新净值/万份收益-报告时间': '2024-11-22',  # 字符串
                '申购状态': '开放申购',
                '赎回状态': '开放赎回',
                '下一开放日': None,  # None值
                '购买起点': 10.0,
                '日累计限定金额': 100000000.0,
                '手续费': 0.08
            }
        ])
        print("   ✅ 测试数据创建成功")
        print(f"      记录1: 下一开放日={test_data.iloc[0]['下一开放日']}, 类型={type(test_data.iloc[0]['下一开放日'])}")
        print(f"      记录2: 下一开放日={test_data.iloc[1]['下一开放日']}, 类型={type(test_data.iloc[1]['下一开放日'])}")
    except Exception as e:
        print(f"   ❌ 创建测试数据失败: {e}")
        return False
    
    # 3. 测试保存数据（之前会报错的操作）
    print("\n3. 测试保存数据到MongoDB...")
    try:
        saved = await service.save_fund_purchase_status_data(test_data)
        print(f"   ✅ 数据保存成功，保存了 {saved} 条记录")
        print("      这证明datetime.date对象已被正确转换为字符串")
    except Exception as e:
        print(f"   ❌ 保存数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. 验证保存的数据
    print("\n4. 验证保存的数据类型...")
    try:
        collection = db.get_collection("fund_purchase_status")
        
        # 检查第一条记录
        doc1 = await collection.find_one({'基金代码': 'TEST999'})
        if doc1:
            next_open_date = doc1.get('下一开放日')
            report_time = doc1.get('最新净值/万份收益-报告时间')
            print(f"   ✅ 记录1验证:")
            print(f"      下一开放日: {next_open_date}, 类型: {type(next_open_date)}")
            print(f"      报告时间: {report_time}, 类型: {type(report_time)}")
            
            # 验证是字符串类型
            assert isinstance(next_open_date, str), f"下一开放日应该是字符串，但是 {type(next_open_date)}"
            assert next_open_date == '2025-12-08', f"日期格式错误: {next_open_date}"
            print("      ✅ 日期字段已正确转换为字符串格式 'YYYY-MM-DD'")
        
        # 检查第二条记录
        doc2 = await collection.find_one({'基金代码': 'TEST1000'})
        if doc2:
            next_open_date = doc2.get('下一开放日')
            print(f"   ✅ 记录2验证:")
            print(f"      下一开放日: {next_open_date}, 类型: {type(next_open_date)}")
            assert next_open_date is None, f"None值应该保持None，但是 {next_open_date}"
            print("      ✅ None值正确保持")
            
    except Exception as e:
        print(f"   ❌ 验证数据失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 5. 清理测试数据
    print("\n5. 清理测试数据...")
    try:
        collection = db.get_collection("fund_purchase_status")
        result = await collection.delete_many({'基金代码': {'$in': ['TEST999', 'TEST1000']}})
        print(f"   ✅ 测试数据清理成功，删除了 {result.deleted_count} 条记录")
    except Exception as e:
        print(f"   ⚠️  清理测试数据失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！datetime.date编码问题已修复")
    print("=" * 60)
    print("\n修复说明:")
    print("- datetime.date对象已正确转换为'YYYY-MM-DD'格式的字符串")
    print("- None值正确保持为None")
    print("- 不再出现'cannot encode object: datetime.date'错误")
    
    return True


async def main():
    """主函数"""
    try:
        success = await test_datetime_conversion()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
