from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import StagehandTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from dotenv import load_dotenv
from typing import List
import os


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Usta():
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
    def web_scraper(self) -> Agent:
        with StagehandTool(
            api_key=os.getenv("BROWSERBASE_API_KEY"),
            project_id=os.getenv("BROWSERBASE_PROJECT_ID"),
            model_api_key=os.getenv("ANTHROPIC_API_KEY"),  # OpenAI or Anthropic API key
        ) as stagehand_tool:
            return Agent(
            config=self.agents_config['web_scraper'], # type: ignore[index]
            verbose=True,
            tools=[stagehand_tool]
            )

    @agent
    def data_visualization_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['data_visualization_specialist'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def web_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['web_scraping_task'], # type: ignore[index]
            output_file='tournaments.json',
            allow_code_execution=True, # Allows the agent to execute code if needed
        )

    @task
    def data_visualization_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_visualization_task'], # type: ignore[index]
            output_file='map.html'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Usta crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
