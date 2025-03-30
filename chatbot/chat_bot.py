from prompt_generator import PromptGenerator
from aiven_database import get_aiven_db
from langchain.chains import create_sql_query_chain
from llms import GoogleLLM, DeepSeekLLM, OpenAILLM
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_verbose, set_debug
from prefix_generator import get_set_up_prediction_prefix
from router import ChainRouter


# self.__llm = GoogleLLM('gemini-2.0-flash-lite', 0.0).get_llm()
# self.__llm = GoogleLLM('gemini-2.5-pro-exp-03-25', 0.0).get_llm()
# self.__llm = GoogleLLM('gemini-2.0-flash', 0.0).get_llm()
# self.__llm = DeepSeekLLM('deepseek-chat', 0.0).get_llm()
# self.__llm = OpenAILLM('davinci-002', 0.0).get_llm()

class ChatBot:

    def __init__(self):
        # set_debug(True)
        # set_verbose(True)
        self.__prompt_generator = PromptGenerator()
        self.__llm = GoogleLLM('gemini-2.0-flash-lite', 0.0).get_llm()
        self.__db = get_aiven_db()
        self.__sql_toolkit = SQLDatabaseToolkit(db=self.__db, llm=self.__llm)
        self.__sql_agent = create_sql_agent(llm=self.__llm, toolkit=self.__sql_toolkit, verbose=True)
        self.__set_up_sql_agent = create_sql_agent(llm=self.__llm, toolkit=self.__sql_toolkit, verbose=True,
                                                   prefix=get_set_up_prediction_prefix())
        self.__router = self.__get_router()
        self.__run()

    def __get_router(self):
        classification_prompt = self.__prompt_generator.get_classification_prompt()
        classification_chain = classification_prompt | self.__llm | StrOutputParser()
        prediction_prompt = self.__prompt_generator.get_prediction_prompt()
        prediction_chain = prediction_prompt | self.__llm | StrOutputParser()
        return ChainRouter(classification_chain, prediction_chain, self.__sql_agent, self.__set_up_sql_agent)

    def __get_full_chain(self):
        return (RunnablePassthrough.assign(classification=lambda x: self.__router.route_query(x)) |
                RunnableLambda(
                    lambda x:
                    (self.__router.handle_retrieval(x) if x["classification"] == "retrieval"
                     else self.__router.handle_prediction(x) if x["classification"] == "prediction"
                    else self.__router.handle_other(x))))

    def __run(self):
        # question = "What will be the sales for next year in Ecuador for Minty Pop?"
        full_chain = self.__get_full_chain()

        while True:
            question = input("Enter your question > ")

            if question.lower() == "quit":
                break

            result = full_chain.invoke({"question": question})
            print(result)


if __name__ == "__main__":
    ChatBot()
