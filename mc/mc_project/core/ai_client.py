from abc import ABC, abstractmethod

class AiClient(ABC):
    @abstractmethod
    def chat(self, system_msg: str, prompt: str, temperature: float = 0.3, model: str = None) -> str:
        pass
