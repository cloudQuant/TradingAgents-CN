"""
测试 fund_portfolio_hold_em 批量更新修复

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


async def test_batch_update():
    """测试批量更新功能"""
    
    print("=" * 80)
    print("测试 fund_portfolio_hold_em 批量更新修复")
    print("=" * 80)
    
    # 初始化
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    # 创建测试任务
    task_id = task_manager.create_task(
        task_type="test_fund_portfolio_hold_em",
        description="测试批量更新修复"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 开始测试批量更新（限制2024年，前3只基金）...\n")
    
    try:
        # 测试参数：只更新2024年，并发数3
        params = {
            'batch': True,
            'year': '2024',  # 只测试2024年
            'concurrency': 3
        }
        
        # 执行批量更新
        result = await refresh_service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print("\n" + "=" * 80)
        print("测试结果:")
        print("=" * 80)
        print(f"✓ 成功: {result.get('success')}")
        print(f"✓ 保存记录数: {result.get('saved', 0)}")
        print(f"✓ 成功任务数: {result.get('success_count', 0)}")
        print(f"✓ 失败任务数: {result.get('failed_count', 0)}")
        print(f"✓ 跳过任务数: {result.get('skipped_count', 0)}")
        print(f"✓ 总可能组合: {result.get('total_possible', 0)}")
        print(f"✓ 实际更新数: {result.get('total_tasks', 0)}")
        print(f"✓ 消息: {result.get('message', '')}")
        
        # 检查任务状态
        task = task_manager.get_task(task_id)
        print(f"\n任务状态: {task.get('status')}")
        print(f"任务消息: {task.get('message')}")
        
        if result.get('success') and result.get('failed_count', 0) == 0:
            print("\n✅ 测试通过：批量更新成功，没有失败任务！")
            return True
        elif result.get('success'):
            print(f"\n⚠️ 测试部分通过：批量更新完成，但有 {result.get('failed_count', 0)} 个任务失败")
            return True
        else:
            print("\n❌ 测试失败：批量更新异常")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_small_batch():
    """测试小批量更新（更精确的测试）"""
    
    print("\n" + "=" * 80)
    print("测试小批量更新（单个基金代码，2024年）")
    print("=" * 80)
    
    # 初始化
    db = get_mongo_db()
    task_manager = TaskManager()
    refresh_service = FundRefreshService(db)
    
    # 创建测试任务
    task_id = task_manager.create_task(
        task_type="test_single_fund",
        description="测试单个基金更新"
    )
    
    print(f"\n[+] 任务ID: {task_id}")
    print(f"[+] 测试单个基金代码更新...\n")
    
    try:
        # 测试参数：单个基金代码
        params = {
            'fund_code': '000001',  # 华夏成长
            'year': '2024'
        }
        
        # 执行单个更新
        result = await refresh_service._refresh_fund_portfolio_hold_em(task_id, params)
        
        print("\n" + "=" * 80)
        print("测试结果:")
        print("=" * 80)
        print(f"✓ 成功: {result.get('success')}")
        print(f"✓ 保存记录数: {result.get('saved', 0)}")
        print(f"✓ 基金代码: {result.get('fund_code', '')}")
        print(f"✓ 年份: {result.get('year', '')}")
        print(f"✓ 消息: {result.get('message', '')}")
        
        if result.get('success'):
            print("\n✅ 单个基金更新测试通过！")
            return True
        else:
            print("\n❌ 单个基金更新测试失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n🚀 开始测试 fund_portfolio_hold_em 批量更新修复\n")
    
    # 测试1: 单个基金更新
    test1_result = await test_small_batch()
    
    # 如果单个测试通过，再测试批量
    if test1_result:
        # 测试2: 批量更新
        test2_result = await test_batch_update()
        
        if test2_result:
            print("\n" + "=" * 80)
            print("🎉 所有测试通过！批量更新修复成功！")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("⚠️ 批量更新测试失败，需要进一步调查")
            print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("⚠️ 单个基金更新测试失败，请先检查基础功能")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
