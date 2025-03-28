from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

class PromptGenerator:

    @staticmethod
    def get_classification_prompt():
        classification_prompt = PromptTemplate.from_template(
            """
                You are an experienced Data Analyst. This is a chat for a confectionery business related topics only.
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
                You are an experienced data analyst. Perform the requested prediction/analysis based on this data:

                <sql_result>
                {sql_result}
                </sql_result>

                <question>
                {question}
                </question>

                Provide your prediction/analysis in a clear, professional manner:
            """
        )
        return prediction_prompt