from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from story_insights.tools.data_analyst import analyze_data# Check our tools documentation for more information on how to use them

from appconfig import AppConfig
from azureai import AzureAI
# Uncomment the following line to use an example of a custom tool
# from story_insights.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

env = AppConfig()
llm = AzureAI(config=env).get_client()

@CrewBase
class StoryInsights():
	"""StoryInsights crew"""

	# agents_config = 'config/agents.yaml'
	# tasks_config = 'config/tasks.yaml'

	llm = None 

	@classmethod
	def initialize_llm(cls):
		env = AppConfig()
		cls.llm = AzureAI(config=env).get_client()

	@agent
	def data_analyst(self) -> Agent:
         return Agent(
                config=self.agents_config['data_analyst_agent'],
                llm=self.llm,
                tools=[analyze_data], # Example of tool usage
                verbose=True
            )

	# @agent
	# def reporting_analyst(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config['reporting_analyst'],
	# 		verbose=True
	# 	)

	@task
	def data_analysis_task(self) -> Task:
			return Task(
				config=self.tasks_config['data_analysis_task']
			)

	# @task
	# def reporting_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['reporting_task'],
	# 		output_file='report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the StoryInsights crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
