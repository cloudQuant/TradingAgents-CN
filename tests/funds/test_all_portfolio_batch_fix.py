"""
测试所有基金持仓集合的批量更新优化

验证分批处理修复是否解决了批量更新失败的问题
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.services.fund_refresh_service import FundRefreshService
from app.utils.task_manager import TaskManager
from app.core.database import get_mongo_db


async def test_fund_portfolio_hold_em():
    """测试 fund_portfolio_hold_em 批量更新"""
    
    print("\n" + "=" * 80)
    print("测试 1: fund_portfolio_hold_em（基金持仓-东财）")
    print("=" * 80)
    
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    task_id = task_manager.create_task(
        task_type="test_fund_portfolio_hold_em",
        description="测试基金持仓批量更新"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 测试参数: 2024年, 并发数3")
    
    try:
        params = {
            'batch': True,
            'year': '2024',
            'concurrency': 3
        }
        
        result = await refresh_service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print("\n结果:")
        print(f"  ✓ 成功: {result.get('success')}")
        print(f"  ✓ 保存: {result.get('saved', 0)} 条")
        print(f"  ✓ 成功任务: {result.get('success_count', 0)}")
        print(f"  ✓ 失败任务: {result.get('failed_count', 0)}")
        print(f"  ✓ 跳过任务: {result.get('skipped_count', 0)}")
        
        success = result.get('success', False)
        if success:
            print("\n✅ fund_portfolio_hold_em 测试通过！")
        else:
            print("\n❌ fund_portfolio_hold_em 测试失败")
        return success
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fund_portfolio_bond_hold_em():
    """测试 fund_portfolio_bond_hold_em 批量更新"""
    
    print("\n" + "=" * 80)
    print("测试 2: fund_portfolio_bond_hold_em（基金债券持仓-东财）")
    print("=" * 80)
    
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    task_id = task_manager.create_task(
        task_type="test_fund_portfolio_bond_hold_em",
        description="测试债券持仓批量更新"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 测试参数: 2024年, 并发数3")
    
    try:
        params = {
            'batch': True,
            'year': '2024',
            'concurrency': 3
        }
        
        result = await refresh_service._refresh_fund_portfolio_bond_hold_em(task_id, params)
        
        print("\n结果:")
        print(f"  ✓ 成功: {result.get('success')}")
        print(f"  ✓ 保存: {result.get('saved', 0)} 条")
        print(f"  ✓ 成功任务: {result.get('success_count', 0)}")
        print(f"  ✓ 失败任务: {result.get('failed_count', 0)}")
        print(f"  ✓ 跳过任务: {result.get('skipped_count', 0)}")
        
        success = result.get('success', False)
        if success:
            print("\n✅ fund_portfolio_bond_hold_em 测试通过！")
        else:
            print("\n❌ fund_portfolio_bond_hold_em 测试失败")
        return success
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fund_portfolio_industry_allocation_em():
    """测试 fund_portfolio_industry_allocation_em 批量更新"""
    
    print("\n" + "=" * 80)
    print("测试 3: fund_portfolio_industry_allocation_em（基金行业配置-东财）")
    print("=" * 80)
    
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    task_id = task_manager.create_task(
        task_type="test_fund_portfolio_industry_allocation_em",
        description="测试行业配置批量更新"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 测试参数: 2024-12-31, 并发数3")
    
    try:
        params = {
            'batch': True,
            'year': '2024',  # 会转换为 2024-12-31
            'concurrency': 3
        }
        
        result = await refresh_service._refresh_fund_portfolio_industry_allocation_em(task_id, params)
        
        print("\n结果:")
        print(f"  ✓ 成功: {result.get('success')}")
        print(f"  ✓ 保存: {result.get('saved', 0)} 条")
        print(f"  ✓ 成功任务: {result.get('success_count', 0)}")
        print(f"  ✓ 失败任务: {result.get('failed_count', 0)}")
        print(f"  ✓ 跳过任务: {result.get('skipped_count', 0)}")
        
        success = result.get('success', False)
        if success:
            print("\n✅ fund_portfolio_industry_allocation_em 测试通过！")
        else:
            print("\n❌ fund_portfolio_industry_allocation_em 测试失败")
        return success
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_single_fund_update():
    """测试单个基金更新（确保基础功能正常）"""
    
    print("\n" + "=" * 80)
    print("测试 0: 单个基金更新（基础功能验证）")
    print("=" * 80)
    
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    task_id = task_manager.create_task(
        task_type="test_single_fund",
        description="测试单个基金持仓更新"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 测试基金: 000001（华夏成长），年份: 2024")
    
    try:
        params = {
            'fund_code': '000001',
            'year': '2024'
        }
        
        result = await refresh_service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print("\n结果:")
        print(f"  ✓ 成功: {result.get('success')}")
        print(f"  ✓ 保存: {result.get('saved', 0)} 条")
        print(f"  ✓ 消息: {result.get('message', '')}")
        
        success = result.get('success', False)
        if success:
            print("\n✅ 单个基金更新测试通过！")
        else:
            print("\n❌ 单个基金更新测试失败")
        return success
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    
    print("\n" + "🚀" * 40)
    print("基金持仓集合批量更新优化测试")
    print("🚀" * 40)
    
    results = {}
    
    # 测试0: 单个基金更新（基础功能）
    print("\n开始基础功能测试...")
    results['single'] = await test_single_fund_update()
    
    if not results['single']:
        print("\n" + "⚠️" * 40)
        print("警告：单个基金更新失败，建议先检查基础功能")
        print("⚠️" * 40)
        return
    
    # 测试1: fund_portfolio_hold_em
    print("\n开始批量更新测试...")
    results['hold'] = await test_fund_portfolio_hold_em()
    
    # 等待一段时间，避免API限流
    print("\n⏳ 等待5秒，避免API限流...")
    await asyncio.sleep(5)
    
    # 测试2: fund_portfolio_bond_hold_em
    results['bond'] = await test_fund_portfolio_bond_hold_em()
    
    # 等待一段时间
    print("\n⏳ 等待5秒，避免API限流...")
    await asyncio.sleep(5)
    
    # 测试3: fund_portfolio_industry_allocation_em
    results['industry'] = await test_fund_portfolio_industry_allocation_em()
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    test_names = {
        'single': '单个基金更新',
        'hold': 'fund_portfolio_hold_em',
        'bond': 'fund_portfolio_bond_hold_em',
        'industry': 'fund_portfolio_industry_allocation_em'
    }
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for key, name in test_names.items():
        status = "✅ 通过" if results.get(key) else "❌ 失败"
        print(f"  {status}: {name}")
    
    print("\n" + "-" * 80)
    print(f"总计: {passed}/{total} 个测试通过")
    print("-" * 80)
    
    if passed == total:
        print("\n🎉 恭喜！所有测试通过！批量更新优化成功！")
    else:
        print(f"\n⚠️ 有 {total - passed} 个测试失败，请检查日志")
    
    print("\n说明:")
    print("  - 批量更新采用分批处理模式（BATCH_SIZE=100）")
    print("  - 每批次通过 Semaphore 限制并发数（默认3）")
    print("  - 使用增量更新，只更新缺失数据")
    print("  - API调用添加0.3秒延迟，避免限流")


if __name__ == "__main__":
    asyncio.run(main())
