from chatbot.llms.llm import LLM
from langchain_openai import OpenAI

class OpenAILLM(LLM):
    def get_environment_variable_name(self):
        return 'OPENAI_API_KEY'

    def get_llm(self):
        return OpenAI(
            model=self._model,
            temperature=self._temperature
        )
