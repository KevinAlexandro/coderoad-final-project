from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX


def get_set_up_prediction_prefix():
    set_up_prefix = """
    \nYou will be provided a prediction question. Do not make the prediction. The database has only raw_data up until 2024-12-31 (inclusive). Do not query for raw_data after 2024-12-31.    
    Retrieve historical raw_data from previous years that could lead to an informed prediction. Summarize the retrieved raw_data by grouping it by year, month (same month in different years) or day (same day in different years) and/or apply central tendency metrics if needed.  
    Afterwards, reply such raw_data (data_retrieved) using the following format:
    <description>
    Give a description about the raw_data retrieved
    </description>
    <raw_data>
    data_retrieved
    </raw_data>
    """
    return SQL_PREFIX + set_up_prefix
