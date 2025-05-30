import asyncio
from typing import Dict, List, Optional
from agent import Agent
from communication import CommunicationLayer
from task_scheduler import TaskScheduler

class AgentManager:
    def __init__(self, communication_layer: CommunicationLayer, task_scheduler: TaskScheduler):
        self.agents: Dict[str, Agent] = {}
        self.communication_layer = communication_layer
        self.task_scheduler = task_scheduler
        self.running = False

    async def register_agent(self, agent: Agent) -> bool:
        """注册新的智能体"""
        if agent.agent_id in self.agents:
            return False
        
        self.agents[agent.agent_id] = agent
        # 注册到通信层
        await self.communication_layer.register_agent(agent.agent_id)
        print(f"Agent {agent.agent_id} registered successfully")
        return True

    async def unregister_agent(self, agent_id: str) -> bool:
        """注销智能体"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        await agent.stop()
        del self.agents[agent_id]
        await self.communication_layer.unregister_agent(agent_id)
        print(f"Agent {agent_id} unregistered successfully")
        return True

    async def start_agent(self, agent_id: str) -> bool:
        """启动特定智能体"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        await agent.start()
        return True

    async def stop_agent(self, agent_id: str) -> bool:
        """停止特定智能体"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        await agent.stop()
        return True

    async def start_all(self):
        """启动所有智能体"""
        self.running = True
        tasks = []
        
        # 启动所有智能体
        for agent in self.agents.values():
            tasks.append(agent.start())
        
        if tasks:
            await asyncio.gather(*tasks)
        
        print(f"Started {len(self.agents)} agents")

    async def stop_all(self):
        """停止所有智能体"""
        self.running = False
        tasks = []
        
        # 停止所有智能体
        for agent in self.agents.values():
            tasks.append(agent.stop())
        
        if tasks:
            await asyncio.gather(*tasks)
        
        print("All agents stopped")

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取指定智能体"""
        return self.agents.get(agent_id)

    def list_agents(self) -> List[str]:
        """列出所有智能体ID"""
        return list(self.agents.keys())

    def get_agent_status(self, agent_id: str) -> Optional[str]:
        """获取智能体状态"""
        agent = self.agents.get(agent_id)
        return agent.status if agent else None

    async def broadcast_message(self, message: str, sender_id: Optional[str] = None):
        """向所有智能体广播消息"""
        for agent_id in self.agents.keys():
            if agent_id != sender_id:  # 不发送给自己
                await self.communication_layer.send_message(
                    sender_id or "system", 
                    agent_id, 
                    message
                )
