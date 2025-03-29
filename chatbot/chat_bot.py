from prompt_generator import PromptGenerator
from aiven_database import get_aiven_db
from langchain.chains import create_sql_query_chain
from google_llm import GoogleLLM
from langchain.schema.runnable import RunnableBranch, RunnablePassthrough
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.runnables import RunnableLambda
from typing import Literal, Dict
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_verbose

# self.__gemini_2_0_f_lite = GoogleLLM('gemini-2.0-flash-lite', 0.0).get_llm()
# self.__gemini_2_5_pro_exp = GoogleLLM('gemini-2.5-pro-exp-03-25', 0.0).get_llm()
# self.__gemini_2_0_f = GoogleLLM('gemini-2.0-flash', 0.0).get_llm()

class ChatBot:

    def route_query(self, info: Dict) -> Literal["retrieval", "prediction", "other"]:
        question = info["question"]
        classification = self.__classification_chain.invoke({"question": question})
        return classification

    def handle_retrieval(self, info: Dict):
        question = info["question"]
        return self.__sql_agent.invoke({"input": question})

    def handle_prediction(self, info: Dict):
        question = info["question"]
        # First get data from SQL
        sql_result = self.__sql_agent.invoke({"input": question})
        # Then analyze it
        return self.__prediction_chain.invoke({"question": question, "sql_result": sql_result})

    def handle_other(self, info: Dict):
        return "I don't know"

    def __init__(self):
        set_verbose(True)
        self.__prompt_generator = PromptGenerator()
        self.__gemini = GoogleLLM('gemini-2.0-flash', 0.0).get_llm()
        self.__db = get_aiven_db()
        self.__sql_toolkit = SQLDatabaseToolkit(db=self.__db, llm=self.__gemini)
        self.__sql_agent = create_sql_agent(llm=self.__gemini, toolkit=self.__sql_toolkit)
        classification_prompt = self.__prompt_generator.get_classification_prompt()
        self.__classification_chain = classification_prompt | self.__gemini | StrOutputParser()
        prediction_prompt = self.__prompt_generator.get_prediction_prompt()
        self.__prediction_chain = prediction_prompt | self.__gemini | StrOutputParser()
        self.__run()

    def __invoke_agent(self, query: str):
        return self.__sql_agent.invoke({'input': query})['output']

    def __run(self):
        full_chain = (RunnablePassthrough.assign(classification=lambda x: self.route_query(x)) |
                      RunnableLambda(
                          lambda x:
                          (self.handle_retrieval(x) if x["classification"] == "retrieval"
                          else self.handle_prediction(x) if x["classification"] == "prediction"
                          else self.handle_other(x))))

        question = "What will be the sales for next year in Ecuador for Minty?"
        result = full_chain.invoke({"question": question})
        print(result)

if __name__ == "__main__":
    ChatBot()

