from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX


# When replying SQL code do not enclose it in any tag like 'sql' or 'text'. Simple provide the SQL code.
def get_set_up_prediction_prefix():
    set_up_prefix = """
     When replying SQL code do not enclose it in any tag like 'sql' or 'text'. Simply provide the SQL code.
    \nYou will be provided a prediction question. Do not make the prediction. The database has only data up until 2024-12-31 (inclusive). Do not query for data after 2024-12-31.    
    Retrieve and summarize historical data keeping data fidelity as much as possible. Also, look for the historical popularity score of the product and also attach it. Summarize the retrieved data by grouping it by year, month (same month in different years) or day (same day in different years) and/or apply central tendency metrics if needed.  
    Afterwards, reply with such data (data_retrieved) like this:
    ########### Start of Description ###########
    Give a description about the data_retrieved
    ########### End of Description ###########
    Data retrieved:
    ########### Start of data_retrieved ###########
    data_retrieved
    ########### End of data_retrieved ###########
    """
    return SQL_PREFIX + set_up_prefix
