from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.memory_manager import MemoryManager
from .tools.custom_tool import search_food_facts
from crewai import FileSearchTool
@CrewBase
class BalancedLifeCrew:
    """BalancedLife crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self, agents: List[BaseAgent], tasks: List[Task]):
        self.agents = agents
        self.tasks = tasks
        self.agents_config = {
            'orchestrator': 'student_clash/agents/orchestrator.yaml',
            'trainer': 'student_clash/agents/trainer.yaml',
            'nutritionist': 'student_clash/agents/nutritionist.yaml',
        }
        self.memory_manager = MemoryManager()
        self.training_tool = FileSearchTool(
            description="Tool for accessing fitness training guidelines and workout plans.",
            config={
                "search_tool": {
                    "dir_path": "knowledge/fitness" # PUNTA ALLA CARTELLA
                }
            }
        )
        
        # Tool per il Nutrizionista: accede a tutti i file nella cartella 'nutrition'
        self.nutrition_tool = FileSearchTool(
            description="Tool for accessing official nutritional guidelines and food tables.",
            config={
                "search_tool": {
                    "dir_path": "knowledge/nutrition" # PUNTA ALLA CARTELLA
                }
            }
        )
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools


    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'], 
            allow_delegation=True,
            memory=True,
            verbose=True
        )
    @agent
    def trainer(self) -> Agent:
        memory = self.memory_manager.memory
        return Agent(
            config=self.agents_config['trainer'], 
            tools=[self.trainer_tool],
            memory=memory,
            verbose=True
        )

    @agent
    def nutritionist(self) -> Agent:
        memory = self.memory_manager.memory
        return Agent(
            config=self.agents_config['nutritionist'], 
            tools=[self.nutritionist_tool, search_food_facts],
            memory=memory,
            verbose=True
        )


     # leggi da tasks.yaml
    @task
    def fitness_task(self) -> Task:
        task = Task(config=self.tasks_config['fitness_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_workout", result)
        return task

    @task
    def diet_task(self) -> Task:
        task = Task(config=self.tasks_config['diet_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_meal_plan", result)
        return task

    @task
    def stress_task(self) -> Task:
        task = Task(config=self.tasks_config['stress_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_stress_level", result)
        return task

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    
def create_crew():
    """Helper function to create and return the crew"""
    return BalancedLifeCrew().crew()
