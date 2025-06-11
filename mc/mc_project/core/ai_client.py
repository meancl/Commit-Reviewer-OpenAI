from abc import ABC, abstractmethod

class AiClient(ABC):
    @abstractmethod
    def chat(self, system_msg: str, prompt: str, contexts:list=[], stream:bool=True) -> str:
        pass
