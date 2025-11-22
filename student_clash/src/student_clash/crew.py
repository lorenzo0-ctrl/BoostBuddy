from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class BalancedLifeCrew:
    """BalancedLife crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # leggi da agents.yaml
    @agent
    def trainer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['trainer_agent'], 
            verbose=True
        )

    @agent
    def nutritionist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['nutritionist_agent'],
            verbose=True
        )

    @agent
    def stress_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['stress_agent'],
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
