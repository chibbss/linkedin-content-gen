from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_json
from pydantic import BaseModel, Field
from typing import Optional, List, Union
from dotenv import load_dotenv
load_dotenv()

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class FinalLinkedinPost(BaseModel):
    final_post: str = Field(
        ...,
        description="Polished LinkedIn post personalized to the company’s mission, product, or offering."
    )
    inspired_by: Optional[str] = Field(
        default=None,
        description="Reference or summary of the viral post that inspired this one."
    )
    brand_voice_used: Optional[str] = Field(
        default=None,
        description="Short description of the brand voice or tone adopted."
    )
    cta_link: Optional[str] = Field(
        default=None,
        description="Call-to-action link included in the post."
    )


@CrewBase
class LinkedinContentGenerator():
    """LinkedinContentGenerator crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            allow_delegation = False
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'],
            verbose=True,
            allow_delegation=False
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True,
            allow_delegation=False
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['discover_viral_content_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_viral_patterns_task'],

        )

    @task
    def copywriter_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_post_draft_task'],

        )

    @task
    def reviewer_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance_task'],
            output_json = FinalLinkedinPost
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LinkedinContentGenerator crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
