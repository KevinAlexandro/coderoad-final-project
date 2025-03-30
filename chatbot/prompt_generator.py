from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


class PromptGenerator:

    @staticmethod
    def get_classification_prompt():
        classification_prompt = PromptTemplate.from_template(
            """
                You are an experienced raw_data analyst. This is a chat for a confectionery business related topics only.
                Classify the following question as either:
                - "retrieval" (if it requires looking up raw_data)
                - "prediction" (if it requires forecasting/analysis of retrieved raw_data)
                - "other" (if unrelated to raw_data)

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
                You are an experienced raw_data analyst. The following question is asking you to predict sales:

                <question>
                {question}
                </question>
                
                The following set_up_data has two parts:
                - a description of the raw_data retrieved which is provided between the tags <description> and </description>
                - the raw_data retrieved for predicting which is provided between the tags <raw_data> and </raw_data> 
                
                <set_up_data>
                {set_up_data}
                </set_up_data>
                
                Provide an optimistic and a pessimistic scenario. Explain briefly what approached was used for each scenario. 
                Using the raw_data you are given implement common business approaches like linear or exponential regressions. 
                Do not extrapolate data. Do not give recommendations on how to act next.:
            """
        )
        return prediction_prompt
