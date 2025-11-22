from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

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
        return Agent(
            config=self.agents_config['trainer'], 
            tools=[self.trainer_tool],
            memoryv=True,
            verbose=True
        )

    @agent
    def nutritionist(self) -> Agent:
        return Agent(
            config=self.agents_config['nutritionist'], 
            tools=[self.nutritionist_tool],
            memory=True,
            verbose=True
        )


     # leggi da tasks.yaml
    @task
    def fitness_task(self) -> Task:
        return Task(
            config=self.tasks_config['fitness_task'],
        )

    @task
    def diet_task(self) -> Task:
        return Task(
            config=self.tasks_config['diet_task'],
        )

    @task
    def stress_task(self) -> Task:
        return Task(
            config=self.tasks_config['stress_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
