from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits.sql.base import create_sql_agent

class SqlAgent(create_sql_agent):
    def __init__(self, extra_prompt: str):
        super().__init__()




    def get_instance(self):
        return SqlAgent('This is a prediction question. Retrieve historical raw_data that could lead to an informed prediction. Do not make the prediction. Only provide raw_data and short sentences of at most 3 possible approaches to make a prediction.')