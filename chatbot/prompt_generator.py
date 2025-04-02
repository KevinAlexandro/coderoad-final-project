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
                - "other" (if unrelated to the above)

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
                You are an experienced data analyst. The following question is asking you to forecast sales:

                <question>
                {question}
                </question>
                
                The following set_up_data has two parts:
                - a description of the set_up_data retrieved which is provided between the tags <description> and </description>
                - the data retrieved for forecasting which is provided between the tags <set_up_data> and </set_up_data> 
                
                <set_up_data>
                {set_up_data}
                </set_up_data>
                
                Provide an optimistic and a pessimistic scenario. Explain briefly (3 lines at most) what approached was used for each scenario. Do not extrapolate or interpolate data.  
                Using the set_up_data you are given, implement common business approaches. When provided, use the popularity score to help you make your prediction.
                The popularity score ranges from 0 to 100 and is a measure of how popular a product is within the company. i.e.:
                    100 = Top-selling product (≥75th percentile)
                    75 = Above-average (50th-75th percentile)
                    50 = Median performer
                    25 = Below-average (25th-50th percentile)
                    0 = Lowest sales (<25th percentile)
                Key points: Scores compare products within the same month/year (not across time). A score of 80 means the product outsold 80% of peers that month.
                Products with consistent high score mean they are rising stars, stocks should be increased. Products with consistent low scores need actions or be discontinued.
            """
        )
        return prediction_prompt
