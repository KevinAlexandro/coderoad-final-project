from chatbot.llms.llm import LLM
from langchain_google_genai import GoogleGenerativeAI


class GoogleLLM(LLM):
    def get_environment_variable_name(self):
        return 'GOOGLE_API_KEY'

    def get_llm(self):
        return GoogleGenerativeAI(
            model=self._model,
            temperature=self._temperature
        )
