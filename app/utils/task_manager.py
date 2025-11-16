"""
任务状态管理器
用于追踪长时间运行任务的进度
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class TaskStatus:
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class TaskManager:
    """任务管理器，用于追踪任务进度"""
    
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
    
    def create_task(self, task_type: str, description: str = "") -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        self._tasks[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "description": description,
            "status": TaskStatus.PENDING,
            "progress": 0,
            "total": 100,
            "message": "等待开始...",
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None
        }
        return task_id
    
    def start_task(self, task_id: str):
        """开始任务"""
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": TaskStatus.RUNNING,
                "started_at": datetime.now().isoformat(),
                "message": "正在处理..."
            })
    
    def update_progress(self, task_id: str, progress: int, total: int, message: str = ""):
        """更新任务进度"""
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "progress": progress,
                "total": total,
                "message": message or f"进度: {progress}/{total}"
            })
    
    def complete_task(self, task_id: str, result: Any = None, message: str = "完成"):
        """完成任务"""
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": TaskStatus.SUCCESS,
                "progress": self._tasks[task_id]["total"],
                "message": message,
                "completed_at": datetime.now().isoformat(),
                "result": result
            })
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": TaskStatus.FAILED,
                "message": f"失败: {error}",
                "completed_at": datetime.now().isoformat(),
                "error": error
            })
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务状态"""
        return self._tasks.get(task_id)
    
    def delete_task(self, task_id: str):
        """删除任务"""
        if task_id in self._tasks:
            del self._tasks[task_id]
    
    def cleanup_old_tasks(self, max_age_seconds: int = 3600):
        """清理旧任务（默认1小时）"""
        now = datetime.now()
        to_delete = []
        for task_id, task in self._tasks.items():
            if task["completed_at"]:
                completed_at = datetime.fromisoformat(task["completed_at"])
                if (now - completed_at).total_seconds() > max_age_seconds:
                    to_delete.append(task_id)
        
        for task_id in to_delete:
            del self._tasks[task_id]


# 全局任务管理器实例
_task_manager = TaskManager()


def get_task_manager() -> TaskManager:
    """获取任务管理器实例"""
    return _task_manager
