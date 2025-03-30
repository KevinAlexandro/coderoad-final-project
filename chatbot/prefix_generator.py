from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX


def get_set_up_prediction_prefix():
    set_up_prefix = """
    \nYou will be provided a prediction question. Do not make the prediction. The database has only data up until 2024-12-31 (inclusive). Do not query for data after 2024-12-31.    
    Retrieve historical data from previous years that could lead to an informed prediction. Summarize the retrieved data by grouping it by year, month (same month in different years) or day (same day in different years) and/or apply central tendency metrics if needed.  
    Afterwards, reply such data (data_retrieved) using the following format:
    <description>
    Give a description about the data retrieved
    </description>
    <data>
    data_retrieved
    </data>
    Write data_retrieved in a structured format. Do not use JSON.
    """
    return SQL_PREFIX + set_up_prefix
