from core.gemini_client import GeminiClient
from core.openai_client import OpenAiClient

def get_ai_provider(provider_name:str = 'openai'):
        if provider_name == 'openai':
            return OpenAiClient()
        elif provider_name == 'gemini':
             return GeminiClient()
        else:
            raise KeyError(f"{provider_name} 모델을 제공하지 않습니다.")