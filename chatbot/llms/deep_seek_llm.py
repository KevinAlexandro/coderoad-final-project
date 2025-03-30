from chatbot.llms.llm import LLM
from langchain_deepseek import ChatDeepSeek


class DeepSeekLLM(LLM):
    def __init__(self, model_name: str, temperature: float):
        super().__init__(model_name, temperature)

    def get_environment_variable_name(self):
        return 'DEEPSEEK_API_KEY'

    def get_llm(self):
        return ChatDeepSeek(
            model=self._model,
            temperature=self._temperature
        )
