from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


class PromptGenerator:

    @staticmethod
    def get_classification_prompt():
        classification_prompt = PromptTemplate.from_template(
            """
                You are an experienced data analyst. This is a chat for a confectionery business related topics only.
                Classify the following question as either:
                - "retrieval" (if it requires looking up data)
                - "prediction" (if it requires forecasting/analysis of retrieved data)
                - "other" (if unrelated to data)

                <question>
                {question}
                </question>

                Respond ONLY with one of these three words: retrieval, prediction, or other.
            """
        )
        return classification_prompt

    @staticmethod
    def get_prediction_prompt():
        prediction_prompt = ChatPromptTemplate.from_template(
            """
                You are an experienced data analyst. The following question is asking you to predict sales:

                <question>
                {question}
                </question>
                
                The following set_up_data has two parts:
                - a description of the data retrieved which is provided between the tags <description> and </description>
                - the data retrieved for predicting which is provided between the tags <data> and </data> 
                
                <set_up_data>
                {set_up_data}
                </set_up_data>

                Provide an optimistic and a pessimistic scenario. Only use the data you are given. Use most common business approaches:
            """
        )
        return prediction_prompt
