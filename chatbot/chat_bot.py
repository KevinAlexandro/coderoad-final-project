from aiven_database import get_aiven_db
from langchain.chains import create_sql_query_chain
from google_llm import GoogleLLM
from langchain.schema.runnable import RunnableBranch
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# self.__gemini_2_0_f_lite = GoogleLLM('gemini-2.0-flash-lite', 0.0).get_llm()
# self.__gemini_2_5_pro_exp = GoogleLLM('gemini-2.5-pro-exp-03-25', 0.0).get_llm()
# self.__gemini_2_0_f = GoogleLLM('gemini-2.0-flash', 0.0).get_llm()

class ChatBot:
    def __init__(self):
        self.__gemini = GoogleLLM('gemini-2.0-flash-lite', 0.0).get_llm()
        self.__db = get_aiven_db()
        self.__sql_toolkit = SQLDatabaseToolkit(db=self.__db, llm=self.__gemini)
        self.__sql_agent = create_sql_agent(llm=self.__gemini, toolkit=self.__sql_toolkit, verbose=True)
        self.__run()
        # result = self.runnable_pipeline(csv_path, query_prompt)

    def runnable_pipeline(self, csv_path, query_prompt):
        sql_chain = self.get_sql_chain()  # SQL Chain

        branch = RunnableBranch(
            (lambda x: "total sales" in x["query"], sql_chain),
            (lambda x: "average price" in x["query"], sql_chain),
            sql_chain  # Default chain
        )

        return branch.invoke({"query": query_prompt})

    def __invoke_agent(self, query: str):
        return self.__sql_agent.invoke({'input': query})['output']


    def __run(self):
        while True:
            query = input("Ask about the data > ")
            print(self.__invoke_agent(query))


if __name__ == "__main__":
    ChatBot()

# query_chain = create_sql_query_chain(gemini_2_0_f, db)
# question = "What is the day with most quantity of sales?"
# sql_query = query_chain.invoke({"question": question})
# print(sql_query)


# sales_str = sales_df.to_string()
#
# template = """
#     If you don't know the answer or the answer cannot be inferred say "I do not know". Else, answer and provide no reasoning at all.
#     You are an expert data analyst. Base your answers only in the following csv data.
#     {csv}
#     {question}
# """
#
# master_template = '''
#     You are an expert data analyst. Only answer using data provided by this context.
#     If you don't know the answer, reply "I don't know"
# '''
# prompt = ChatPromptTemplate.from_template(template)
#
# gemini_2_0_f_chain = (
#     prompt
#     | gemini_2_0_f
#     | StrOutputParser()
# )
# # question = 'What is 2 + 2 ?'
# # question = 'What is the day that has the most quantity of sales?'
# while True:
#     question = input('Type your question: ')
#     print(gemini_2_0_f_chain.invoke({'question': question, 'csv': sales_str}))
