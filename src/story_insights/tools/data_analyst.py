from langchain.tools import tool
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain.agents.agent_types import AgentType
from story_insights.appconfig import AppConfig
from story_insights.azureai import AzureAI

env = AppConfig()
llm = AzureAI(config=env).get_client()
df = pd.read_csv('story_insights/data/export1.csv')

print(df.head())

# Create the Pandas DataFrame agent
agent_executor = create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True,
    return_intermediate_steps=True,
    number_of_head_rows=100,
    max_iterations=22,
    max_execution_time=300,
    agent_executor_kwargs={
        'handle_parsing_errors': 'Check your output and make sure it conforms to the action input.'
    }
)

# Wrap it as a tool
@tool('data_analysis')
def analyze_data(query: str) -> str:
    """Analyze the DataFrame based on the provided query."""
    return agent_executor.run(input=query)
