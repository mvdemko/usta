from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, before_kickoff, crew, task
from dotenv import load_dotenv

from usta.tools.code_runners import run_python_from_repo

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class Usta:
    """Usta crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @before_kickoff
    def get_keys(self, inputs):
        load_dotenv()

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def python_code_runner(self) -> Agent:
        return Agent(
            config=self.agents_config["python_code_runner"],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            tools=[run_python_from_repo],
        )

    @agent
    def data_visualization_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["data_visualization_specialist"],  # type: ignore[index]
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def get_usta_tournament_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["get_usta_data_task"],  # type: ignore[index]
            tools=[run_python_from_repo],
            repo_url="https://github.com/mvdemko/data-retrieval",
            script_path="src/data_retrieval/main.py",
            args=["tournaments", "Adult (18+)", "Southern California"],
            allow_code_execution=True,
            verbose=3,
        )

    @task
    def data_visualization_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_visualization_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Usta crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead
            # https://docs.crewai.com/how-to/Hierarchical/
        )
