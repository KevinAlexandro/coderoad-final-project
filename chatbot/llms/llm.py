import os
from abc import abstractmethod

class LLM:
    def __init__(self, model_name: str, temperature: float):
        self._model = model_name
        self._temperature = temperature
        try:
            self.__api_key = os.environ[self.get_environment_variable_name()]  # Raises error if not set
        except KeyError:
            raise KeyError(f"{self.get_environment_variable_name()} environment variable not set")

    @abstractmethod
    def get_environment_variable_name(self):
        pass

    @abstractmethod
    def get_llm(self):
        pass