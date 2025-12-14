#!/usr/bin/env python
"""
修复 option_refresh_service.py 中的 update_task 调用
TaskManager 没有 update_task 方法，需要使用 start_task, update_progress, complete_task, fail_task
"""

def fix_task_manager_calls():
    """修复 TaskManager 调用"""
    file_path = "/Users/yunjinqi/Documents/TradingAgents-CN/app/services/option_refresh_service.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换1: status="running" -> start_task
    old1 = '''            # 更新任务状态
            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="running",
                    message=f"正在更新 {config['display_name']}..."
                )'''
    new1 = '''            # 更新任务状态
            if self.task_manager and task_id:
                self.task_manager.start_task(task_id)'''
    
    # 替换2: status="completed" -> complete_task
    old2 = '''            # 更新任务完成状态
            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="completed",
                    progress=100,
                    message=f"{config['display_name']} 更新完成"
                )'''
    new2 = '''            # 更新任务完成状态
            if self.task_manager and task_id:
                self.task_manager.complete_task(task_id, result, f"{config['display_name']} 更新完成")'''
    
    # 替换3: status="failed" -> fail_task
    old3 = '''            if self.task_manager and task_id:
                await self.task_manager.update_task(
                    task_id,
                    status="failed",
                    message=f"更新失败: {str(e)}"
                )'''
    new3 = '''            if self.task_manager and task_id:
                self.task_manager.fail_task(task_id, f"更新失败: {str(e)}")'''
    
    # 执行替换
    new_content = content
    
    if old1 in new_content:
        new_content = new_content.replace(old1, new1)
        print("✓ 替换1: update_task(running) -> start_task")
    else:
        print("✗ 未找到替换1的内容")
    
    if old2 in new_content:
        new_content = new_content.replace(old2, new2)
        print("✓ 替换2: update_task(completed) -> complete_task")
    else:
        print("✗ 未找到替换2的内容")
    
    if old3 in new_content:
        new_content = new_content.replace(old3, new3)
        print("✓ 替换3: update_task(failed) -> fail_task")
    else:
        print("✗ 未找到替换3的内容")
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n已保存修改到 {file_path}")
    else:
        print("\n没有需要修改的内容")


if __name__ == "__main__":
    fix_task_manager_calls()
