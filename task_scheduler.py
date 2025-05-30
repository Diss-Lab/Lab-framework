import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Task:
    task_id: str
    agent_id: str
    task_type: str
    parameters: Dict
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[any] = None
    error: Optional[str] = None

class TaskScheduler:
    def __init__(self):
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.tasks: Dict[str, Task] = {}
        self.task_handlers: Dict[str, Callable] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.max_concurrent_tasks = 10
        self.running = False

    def register_task_handler(self, task_type: str, handler: Callable):
        """注册任务处理器"""
        self.task_handlers[task_type] = handler
        print(f"Task handler registered for type: {task_type}")

    async def submit_task(self, task: Task) -> bool:
        """提交任务"""
        try:
            if task.task_id in self.tasks:
                print(f"Task {task.task_id} already exists")
                return False

            self.tasks[task.task_id] = task
            
            # 使用负数优先级，因为PriorityQueue是最小堆
            priority = -task.priority.value
            await self.task_queue.put((priority, task.created_at, task))
            
            print(f"Task {task.task_id} submitted for agent {task.agent_id}")
            return True
        except Exception as e:
            print(f"Error submitting task {task.task_id}: {e}")
            return False

    async def start_scheduler(self):
        """启动任务调度器"""
        self.running = True
        print("Task scheduler started")
        
        while self.running:
            try:
                # 控制并发任务数量
                if len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                    continue

                # 获取任务（1秒超时）
                try:
                    priority, created_at, task = await asyncio.wait_for(
                        self.task_queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                # 执行任务
                if task.task_id not in self.running_tasks:
                    task_coroutine = self._execute_task(task)
                    self.running_tasks[task.task_id] = asyncio.create_task(task_coroutine)

            except Exception as e:
                print(f"Error in task scheduler: {e}")
                await asyncio.sleep(1)

    async def _execute_task(self, task: Task):
        """执行单个任务"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            
            print(f"Executing task {task.task_id} for agent {task.agent_id}")

            if task.task_type in self.task_handlers:
                handler = self.task_handlers[task.task_type]
                result = await handler(task)
                
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                
                print(f"Task {task.task_id} completed successfully")
            else:
                raise Exception(f"No handler found for task type: {task.task_type}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
            print(f"Task {task.task_id} failed: {e}")
        
        finally:
            # 清理运行中的任务
            if task.task_id in self.running_tasks:
                del self.running_tasks[task.task_id]

    async def stop_scheduler(self):
        """停止任务调度器"""
        self.running = False
        
        # 等待所有运行中的任务完成
        if self.running_tasks:
            await asyncio.gather(*self.running_tasks.values(), return_exceptions=True)
        
        print("Task scheduler stopped")

    async def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        
        if task.status == TaskStatus.RUNNING:
            if task_id in self.running_tasks:
                self.running_tasks[task_id].cancel()
                del self.running_tasks[task_id]
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()
        
        print(f"Task {task_id} cancelled")
        return True

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)

    def get_agent_tasks(self, agent_id: str) -> List[Task]:
        """获取特定智能体的所有任务"""
        return [task for task in self.tasks.values() if task.agent_id == agent_id]

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self.tasks.values() if task.status == status]

    def get_queue_size(self) -> int:
        """获取队列大小"""
        return self.task_queue.qsize()

    def get_running_task_count(self) -> int:
        """获取运行中的任务数量"""
        return len(self.running_tasks)
