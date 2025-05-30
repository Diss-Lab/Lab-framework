import asyncio
from typing import Dict, Optional, List, Any
from datetime import datetime
from communication import CommunicationLayer, Message
from task_scheduler import TaskScheduler, Task, TaskStatus, TaskPriority

class AgentStatus:
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"
    ERROR = "error"

class Agent:
    def __init__(self, agent_id: str, agent_type: str, 
                 communication_layer: CommunicationLayer, 
                 task_scheduler: TaskScheduler):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.communication_layer = communication_layer
        self.task_scheduler = task_scheduler
        self.status = AgentStatus.OFFLINE
        self.running = False
        self.capabilities: List[str] = []
        self.current_task: Optional[Task] = None
        self.task_history: List[str] = []
        self.error_count = 0
        self.last_activity = datetime.now()

    async def start(self):
        """启动智能体"""
        try:
            self.running = True
            self.status = AgentStatus.IDLE
            self.last_activity = datetime.now()
            
            # 注册到通信层
            await self.communication_layer.register_agent(self.agent_id)
            
            # 注册任务处理器
            self._register_task_handlers()
            
            # 启动消息处理循环
            asyncio.create_task(self._message_loop())
            asyncio.create_task(self._heartbeat_loop())
            
            print(f"Agent {self.agent_id} started successfully")
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.error_count += 1
            print(f"Error starting agent {self.agent_id}: {e}")

    async def stop(self):
        """停止智能体"""
        try:
            self.running = False
            self.status = AgentStatus.OFFLINE
            
            # 取消当前任务
            if self.current_task:
                await self.task_scheduler.cancel_task(self.current_task.task_id)
            
            # 从通信层注销
            await self.communication_layer.unregister_agent(self.agent_id)
            
            print(f"Agent {self.agent_id} stopped")
            
        except Exception as e:
            print(f"Error stopping agent {self.agent_id}: {e}")

    def _register_task_handlers(self):
        """注册任务处理器"""
        # 注册基本任务类型
        self.task_scheduler.register_task_handler(f"{self.agent_type}_task", self._handle_generic_task)
        self.task_scheduler.register_task_handler("communicate", self._handle_communication_task)
        self.task_scheduler.register_task_handler("analyze", self._handle_analysis_task)

    async def _handle_generic_task(self, task: Task) -> Any:
        """处理通用任务"""
        try:
            self.current_task = task
            self.status = AgentStatus.BUSY
            self.last_activity = datetime.now()
            
            # 模拟任务处理
            await asyncio.sleep(1)
            
            # 根据任务类型执行不同逻辑
            result = f"Task {task.task_id} completed by {self.agent_id}"
            
            self.task_history.append(task.task_id)
            self.current_task = None
            self.status = AgentStatus.IDLE
            
            return result
            
        except Exception as e:
            self.error_count += 1
            self.status = AgentStatus.ERROR
            raise e

    async def _handle_communication_task(self, task: Task) -> Any:
        """处理通信任务"""
        try:
            target_agent = task.parameters.get("target_agent")
            message_content = task.parameters.get("message", "Hello")
            
            if target_agent:
                success = await self.communication_layer.send_message(
                    self.agent_id, target_agent, message_content
                )
                return f"Message sent to {target_agent}: {success}"
            else:
                return "Error: No target agent specified"
                
        except Exception as e:
            raise e

    async def _handle_analysis_task(self, task: Task) -> Any:
        """处理分析任务"""
        try:
            data = task.parameters.get("data", [])
            analysis_type = task.parameters.get("type", "basic")
            
            # 模拟数据分析
            await asyncio.sleep(2)
            
            result = {
                "analysis_type": analysis_type,
                "data_size": len(data) if isinstance(data, list) else 0,
                "result": f"Analysis completed by {self.agent_id}"
            }
            
            return result
            
        except Exception as e:
            raise e

    async def _message_loop(self):
        """消息处理循环"""
        while self.running:
            try:
                message = await self.communication_layer.receive_message(
                    self.agent_id, timeout=1.0
                )
                
                if message:
                    await self._process_message(message)
                    self.last_activity = datetime.now()
                    
            except Exception as e:
                print(f"Error in message loop for {self.agent_id}: {e}")
                self.error_count += 1
                await asyncio.sleep(1)

    async def _process_message(self, message: Message):
        """处理接收到的消息"""
        try:
            print(f"Agent {self.agent_id} received message from {message.sender_id}: {message.content}")
            
            # 根据消息类型处理
            if message.message_type == "task_request":
                await self._handle_task_request(message)
            elif message.message_type == "query":
                await self._handle_query(message)
            else:
                # 默认处理
                await self._handle_general_message(message)
                
        except Exception as e:
            print(f"Error processing message for {self.agent_id}: {e}")
            self.error_count += 1

    async def _handle_task_request(self, message: Message):
        """处理任务请求消息"""
        # 这里可以解析消息内容并创建相应的任务
        pass

    async def _handle_query(self, message: Message):
        """处理查询消息"""
        response = f"Agent {self.agent_id} status: {self.status}"
        await self.communication_layer.send_message(
            self.agent_id, message.sender_id, response
        )

    async def _handle_general_message(self, message: Message):
        """处理一般消息"""
        # 默认的消息处理逻辑
        pass

    async def _heartbeat_loop(self):
        """心跳循环"""
        while self.running:
            try:
                self.last_activity = datetime.now()
                await asyncio.sleep(30)  # 每30秒发送一次心跳
            except Exception as e:
                print(f"Error in heartbeat loop for {self.agent_id}: {e}")

    async def submit_task(self, task_type: str, parameters: Dict, 
                         priority: TaskPriority = TaskPriority.NORMAL) -> bool:
        """提交任务"""
        task_id = f"{self.agent_id}_{task_type}_{datetime.now().timestamp()}"
        task = Task(
            task_id=task_id,
            agent_id=self.agent_id,
            task_type=task_type,
            parameters=parameters,
            priority=priority
        )
        
        return await self.task_scheduler.submit_task(task)

    def add_capability(self, capability: str):
        """添加能力"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)

    def remove_capability(self, capability: str):
        """移除能力"""
        if capability in self.capabilities:
            self.capabilities.remove(capability)

    def get_status_info(self) -> Dict:
        """获取状态信息"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "running": self.running,
            "capabilities": self.capabilities,
            "current_task": self.current_task.task_id if self.current_task else None,
            "task_history_count": len(self.task_history),
            "error_count": self.error_count,
            "last_activity": self.last_activity.isoformat()
        }
