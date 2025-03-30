from typing import Literal, Dict
from langchain.agents.agent import AgentExecutor

class ChainRouter:
    def __init__(self, classifier_chain, prediction_chain, sql_agent: AgentExecutor, sql_set_up_agent: AgentExecutor):
        self.__classifier_chain = classifier_chain
        self.__sql_agent = sql_agent
        self.__prediction_chain = prediction_chain
        self.__set_up_sql_agent = sql_set_up_agent

    def route_query(self, info: Dict) -> Literal["retrieval", "prediction", "other"]:
        question = info["question"]
        classification = self.__classifier_chain.invoke({"question": question})
        return classification

    def handle_retrieval(self, info: Dict):
        question = info["question"]
        return self.__sql_agent.invoke({"input": question})

    def handle_prediction(self, info: Dict):
        question = info["question"]
        # First get raw_data from SQL
        set_up_data = self.__set_up_sql_agent.invoke({"input": question})
        print('----------------------------------------------------------')
        print("This is the question: ", question)
        print(set_up_data)
        print('----------------------------------------------------------')

        # Then analyze it
        return self.__prediction_chain.invoke({"question": question, "set_up_data": set_up_data})

    def handle_other(self, info: Dict):
        return "I don't know"