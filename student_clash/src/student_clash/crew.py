from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.memory_manager import MemoryManager
from .tools.custom_tool import search_food_facts
from crewai import FileSearchTool
@CrewBase
class BalancedLifeCrew:
    """BalancedLife crew"""
    
    def __init__(self):
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
            tools=[self.trainer_tool] if hasattr(self, 'trainer_tool') else [],
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
        return Task(
            config=self.tasks_config['fitness_task']
        )

    @task
    def diet_task(self) -> Task:
        return Task(
            config=self.tasks_config['diet_task']
        )

    @task
    def stress_task(self) -> Task:
        return Task(
            config=self.tasks_config['stress_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the crew with memory management callbacks"""
        crew_instance = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
        return crew_instance
    
def create_crew():
    """Helper function to create and return the crew"""
    crew_instance = BalancedLifeCrew()
    return crew_instance.crew()