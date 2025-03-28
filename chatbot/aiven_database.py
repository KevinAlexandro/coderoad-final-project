import os

from langchain_community.utilities import SQLDatabase

def get_aiven_db():
    try:
        connection_string = os.environ["AIVEN_CONNECTION_STRING"]  # Raises error if not set
    except KeyError:
        raise KeyError("AIVEN_CONNECTION_STRING environment variable not set")

    return SQLDatabase.from_uri(connection_string)