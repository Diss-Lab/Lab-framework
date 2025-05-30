import asyncio
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime
    message_type: str = "text"
    priority: int = 0

class CommunicationLayer:
    def __init__(self):
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.registered_agents: set = set()
        self.message_handlers: Dict[str, Callable] = {}
        self.message_history: List[Message] = []
        self.running = False

    async def register_agent(self, agent_id: str):
        """注册智能体到通信层"""
        if agent_id not in self.registered_agents:
            self.message_queues[agent_id] = asyncio.Queue()
            self.registered_agents.add(agent_id)
            print(f"Agent {agent_id} registered to communication layer")

    async def unregister_agent(self, agent_id: str):
        """从通信层注销智能体"""
        if agent_id in self.registered_agents:
            self.registered_agents.remove(agent_id)
            if agent_id in self.message_queues:
                del self.message_queues[agent_id]
            print(f"Agent {agent_id} unregistered from communication layer")

    async def send_message(self, sender_id: str, receiver_id: str, content: str, 
                          message_type: str = "text", priority: int = 0) -> bool:
        """发送消息"""
        if receiver_id not in self.registered_agents:
            print(f"Error: Receiver {receiver_id} not registered")
            return False

        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            timestamp=datetime.now(),
            message_type=message_type,
            priority=priority
        )

        try:
            await self.message_queues[receiver_id].put(message)
            self.message_history.append(message)
            print(f"Message sent from {sender_id} to {receiver_id}: {content[:50]}...")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    async def receive_message(self, agent_id: str, timeout: float = 1.0) -> Optional[Message]:
        """接收消息"""
        if agent_id not in self.message_queues:
            return None

        try:
            message = await asyncio.wait_for(
                self.message_queues[agent_id].get(), 
                timeout=timeout
            )
            return message
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            print(f"Error receiving message for {agent_id}: {e}")
            return None

    async def broadcast_message(self, sender_id: str, content: str, 
                              message_type: str = "broadcast") -> int:
        """广播消息给所有注册的智能体"""
        sent_count = 0
        for receiver_id in self.registered_agents:
            if receiver_id != sender_id:
                success = await self.send_message(
                    sender_id, receiver_id, content, message_type
                )
                if success:
                    sent_count += 1
        return sent_count

    def register_message_handler(self, message_type: str, handler: Callable):
        """注册消息处理器"""
        self.message_handlers[message_type] = handler

    async def process_message(self, message: Message):
        """处理消息"""
        if message.message_type in self.message_handlers:
            try:
                await self.message_handlers[message.message_type](message)
            except Exception as e:
                print(f"Error processing message: {e}")

    def get_message_history(self, agent_id: Optional[str] = None) -> List[Message]:
        """获取消息历史"""
        if agent_id:
            return [msg for msg in self.message_history 
                   if msg.sender_id == agent_id or msg.receiver_id == agent_id]
        return self.message_history.copy()

    def clear_message_history(self):
        """清空消息历史"""
        self.message_history.clear()

    def get_queue_size(self, agent_id: str) -> int:
        """获取消息队列大小"""
        if agent_id in self.message_queues:
            return self.message_queues[agent_id].qsize()
        return 0
