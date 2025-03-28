import os
from langchain_google_genai import GoogleGenerativeAI

class GoogleLLM:
    def __init__(self, model_name: str, temperature: float):
        self.__model = model_name
        self.__temperature = temperature
        try:
            self.__api_key = os.environ["GOOGLE_API_KEY"]  # Raises error if not set
        except KeyError:
            raise KeyError("GOOGLE_API_KEY environment variable not set")

    def get_llm(self):
        return GoogleGenerativeAI(
            model=self.__model,
            temperature=self.__temperature
        )