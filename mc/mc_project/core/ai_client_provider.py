from core import LlamaClient, GeminiClient, OpenAiClient

def get_ai_provider(provider_name:str = 'openai'):
        if provider_name == 'openai':
            return OpenAiClient()
        elif provider_name == 'gemini':
             return GeminiClient()
        elif provider_name == 'llama':
             return LlamaClient()
        else:
            raise KeyError(f"{provider_name} 모델을 제공하지 않습니다.")