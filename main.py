import asyncio
import signal
import sys
from typing import List
from agent import Agent
from agent_manager import AgentManager
from communication import CommunicationLayer
from task_scheduler import TaskScheduler, Task, TaskPriority

class MultiAgentSystem:
    def __init__(self):
        self.communication_layer = CommunicationLayer()
        self.task_scheduler = TaskScheduler()
        self.agent_manager = AgentManager(self.communication_layer, self.task_scheduler)
        self.running = False

    async def initialize(self):
        """初始化系统"""
        try:
            print("Initializing Multi-Agent System...")
            
            # 启动任务调度器
            scheduler_task = asyncio.create_task(self.task_scheduler.start_scheduler())
            
            # 创建示例智能体
            await self._create_sample_agents()
            
            print("System initialized successfully")
            return scheduler_task
            
        except Exception as e:
            print(f"Error initializing system: {e}")
            sys.exit(1)

    async def _create_sample_agents(self):
        """创建示例智能体"""
        agent_configs = [
            {"id": "agent_1", "type": "analyzer"},
            {"id": "agent_2", "type": "communicator"},
            {"id": "agent_3", "type": "processor"}
        ]

        for config in agent_configs:
            agent = Agent(
                agent_id=config["id"],
                agent_type=config["type"],
                communication_layer=self.communication_layer,
                task_scheduler=self.task_scheduler
            )
            
            # 添加能力
            if config["type"] == "analyzer":
                agent.add_capability("data_analysis")
                agent.add_capability("pattern_recognition")
            elif config["type"] == "communicator":
                agent.add_capability("message_routing")
                agent.add_capability("protocol_translation")
            elif config["type"] == "processor":
                agent.add_capability("data_processing")
                agent.add_capability("task_execution")

            await self.agent_manager.register_agent(agent)

    async def start(self):
        """启动系统"""
        try:
            self.running = True
            
            # 初始化系统
            scheduler_task = await self.initialize()
            
            # 启动所有智能体
            await self.agent_manager.start_all()
            
            # 提交一些示例任务
            await self._submit_sample_tasks()
            
            print("Multi-Agent System started successfully")
            print("Press Ctrl+C to stop the system")
            
            # 等待调度器任务
            await scheduler_task
            
        except KeyboardInterrupt:
            print("\nReceived interrupt signal")
        except Exception as e:
            print(f"Error starting system: {e}")
        finally:
            await self.stop()

    async def stop(self):
        """停止系统"""
        if not self.running:
            return
            
        print("Stopping Multi-Agent System...")
        self.running = False
        
        try:
            # 停止所有智能体
            await self.agent_manager.stop_all()
            
            # 停止任务调度器
            await self.task_scheduler.stop_scheduler()
            
            print("System stopped successfully")
            
        except Exception as e:
            print(f"Error stopping system: {e}")

    async def _submit_sample_tasks(self):
        """提交示例任务"""
        try:
            # 分析任务
            analysis_task = Task(
                task_id="analysis_1",
                agent_id="agent_1",
                task_type="analyze",
                parameters={
                    "data": list(range(100)),
                    "type": "statistical"
                },
                priority=TaskPriority.HIGH
            )
            await self.task_scheduler.submit_task(analysis_task)

            # 通信任务
            comm_task = Task(
                task_id="comm_1",
                agent_id="agent_2",
                task_type="communicate",
                parameters={
                    "target_agent": "agent_3",
                    "message": "Hello from agent_2"
                },
                priority=TaskPriority.NORMAL
            )
            await self.task_scheduler.submit_task(comm_task)

            # 处理任务
            process_task = Task(
                task_id="process_1",
                agent_id="agent_3",
                task_type="processor_task",
                parameters={
                    "operation": "data_transform",
                    "input_data": "sample_data"
                },
                priority=TaskPriority.NORMAL
            )
            await self.task_scheduler.submit_task(process_task)

            print("Sample tasks submitted")

        except Exception as e:
            print(f"Error submitting sample tasks: {e}")

    async def status_monitor(self):
        """状态监控"""
        while self.running:
            try:
                print("\n=== System Status ===")
                print(f"Agents: {len(self.agent_manager.list_agents())}")
                print(f"Task Queue Size: {self.task_scheduler.get_queue_size()}")
                print(f"Running Tasks: {self.task_scheduler.get_running_task_count()}")
                
                # 显示智能体状态
                for agent_id in self.agent_manager.list_agents():
                    agent = self.agent_manager.get_agent(agent_id)
                    if agent:
                        status_info = agent.get_status_info()
                        print(f"  {agent_id}: {status_info['status']} (errors: {status_info['error_count']})")
                
                await asyncio.sleep(10)  # 每10秒更新一次状态
                
            except Exception as e:
                print(f"Error in status monitor: {e}")
                await asyncio.sleep(5)

def setup_signal_handlers(system: MultiAgentSystem):
    """设置信号处理器"""
    def signal_handler(signum, frame):
        print(f"\nReceived signal {signum}")
        asyncio.create_task(system.stop())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """主函数"""
    system = MultiAgentSystem()
    
    # 设置信号处理器
    setup_signal_handlers(system)
    
    try:
        # 创建状态监控任务
        monitor_task = asyncio.create_task(system.status_monitor())
        
        # 启动系统
        system_task = asyncio.create_task(system.start())
        
        # 等待任务完成
        await asyncio.gather(system_task, monitor_task, return_exceptions=True)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await system.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
