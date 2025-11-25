#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试终端进度条效果
演示基金持仓和债券持仓批量更新时的终端显示
"""
import asyncio
from tqdm import tqdm
import time

async def demo_fund_portfolio_progress():
    """演示基金持仓批量更新的终端进度条"""
    print("=" * 80)
    print("演示：基金持仓批量更新终端进度条")
    print("=" * 80)
    print()
    
    total_tasks = 100
    success_count = 0
    failed_count = 0
    total_saved = 0
    
    # 创建终端进度条
    pbar = tqdm(total=total_tasks, desc="基金持仓批量更新", unit="任务", 
               bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
    
    for i in range(total_tasks):
        # 模拟处理任务
        await asyncio.sleep(0.05)
        
        # 模拟成功/失败
        if i % 10 == 0:
            failed_count += 1
        else:
            success_count += 1
            saved = (i + 1) * 10
            total_saved += saved
        
        # 更新进度条
        pbar.update(1)
        pbar.set_postfix({
            '成功': success_count, 
            '失败': failed_count,
            '已保存': f'{total_saved}条'
        })
    
    pbar.close()
    print()
    print(f"✅ 完成！总任务: {total_tasks}, 成功: {success_count}, 失败: {failed_count}, 保存: {total_saved}条")
    print()

async def demo_bond_portfolio_progress():
    """演示债券持仓批量更新的终端进度条"""
    print("=" * 80)
    print("演示：债券持仓批量更新终端进度条")
    print("=" * 80)
    print()
    
    total_tasks = 50
    success_count = 0
    failed_count = 0
    total_saved = 0
    
    # 创建终端进度条
    pbar = tqdm(total=total_tasks, desc="债券持仓批量更新", unit="任务", 
               bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
    
    for i in range(total_tasks):
        # 模拟处理任务
        await asyncio.sleep(0.08)
        
        # 模拟成功/失败
        if i % 8 == 0:
            failed_count += 1
        else:
            success_count += 1
            saved = (i + 1) * 8
            total_saved += saved
        
        # 更新进度条
        pbar.update(1)
        pbar.set_postfix({
            '成功': success_count, 
            '失败': failed_count,
            '已保存': f'{total_saved}条'
        })
    
    pbar.close()
    print()
    print(f"✅ 完成！总任务: {total_tasks}, 成功: {success_count}, 失败: {failed_count}, 保存: {total_saved}条")
    print()

async def demo_concurrent_progress():
    """演示并发任务的终端进度条"""
    print("=" * 80)
    print("演示：并发任务处理（模拟实际批量更新）")
    print("=" * 80)
    print()
    
    total_tasks = 30
    concurrency = 5  # 并发数
    success_count = 0
    failed_count = 0
    total_saved = 0
    completed = 0
    
    # 创建终端进度条
    pbar = tqdm(total=total_tasks, desc="并发批量更新", unit="任务", 
               bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')
    
    semaphore = asyncio.Semaphore(concurrency)
    
    async def process_task(task_id):
        nonlocal success_count, failed_count, total_saved, completed
        async with semaphore:
            # 模拟不同任务的处理时间
            await asyncio.sleep(0.1 + (task_id % 3) * 0.05)
            
            # 模拟成功/失败
            if task_id % 7 == 0:
                failed_count += 1
            else:
                success_count += 1
                saved = task_id * 15
                total_saved += saved
            
            completed += 1
            
            # 更新进度条
            pbar.update(1)
            pbar.set_postfix({
                '成功': success_count, 
                '失败': failed_count,
                '已保存': f'{total_saved}条'
            })
    
    # 创建所有任务
    tasks = [process_task(i) for i in range(total_tasks)]
    
    # 并发执行
    try:
        await asyncio.gather(*tasks)
    finally:
        pbar.close()
    
    print()
    print(f"✅ 完成！总任务: {total_tasks}, 成功: {success_count}, 失败: {failed_count}, 保存: {total_saved}条")
    print(f"📊 并发数: {concurrency}, 平均速度: {total_tasks / (total_tasks * 0.15):.2f} 任务/秒")
    print()

async def main():
    """主函数"""
    print()
    print("🚀 终端进度条演示程序")
    print("=" * 80)
    print()
    
    # 演示1：基金持仓
    await demo_fund_portfolio_progress()
    await asyncio.sleep(1)
    
    # 演示2：债券持仓
    await demo_bond_portfolio_progress()
    await asyncio.sleep(1)
    
    # 演示3：并发处理
    await demo_concurrent_progress()
    
    print()
    print("=" * 80)
    print("✨ 所有演示完成！")
    print("=" * 80)
    print()
    print("说明：")
    print("1. 进度条显示：任务名称、百分比、可视化条、已完成/总数")
    print("2. 时间信息：已用时间、剩余时间、处理速率")
    print("3. 实时统计：成功数、失败数、已保存条数")
    print("4. 并发支持：多个任务同时更新进度条")
    print()
    print("在实际应用中，这个进度条会在后端服务运行时显示在终端。")
    print()

if __name__ == "__main__":
    asyncio.run(main())
