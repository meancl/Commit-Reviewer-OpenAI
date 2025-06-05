from ai_git_assistant.openai_client import OpenAiClient

def get_ai_provider(provider_name:str = 'openai'):
        if provider_name == 'openai':
            return OpenAiClient()
        else:
            raise KeyError(f"{provider_name} 모델을 제공하지 않습니다.")