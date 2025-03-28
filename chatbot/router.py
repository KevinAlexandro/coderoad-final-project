from typing import Literal, Dict
from langchain.agents.agent import AgentExecutor

class ChainRouter:
    def __init__(self, classifier_chain, sql_agent: AgentExecutor, prediction_chain):
        self.__classifier_chain = classifier_chain
        self.__sql_agent = sql_agent
        self.__prediction_chain = prediction_chain

    def route_query(self, info: Dict) -> Literal["retrieval", "prediction", "other"]:
        question = info["question"]
        classification = self.__classifier_chain.invoke({"question": question})
        return classification

    def handle_retrieval(self, info: Dict):
        question = info["question"]
        return self.__sql_agent.invoke({"input": question})

    def handle_prediction(self, info: Dict):
        question = info["question"]
        # First get data from SQL
        sql_result = self.__sql_agent.invoke({"input": question})
        # Then analyze it
        return prediction_chain.invoke({"question": question, "sql_result": sql_result})

    def handle_other(info: Dict):
        return "I don't know"