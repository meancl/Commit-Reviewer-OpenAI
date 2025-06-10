from core.ai_client import AiClient

class OpenAiClient(AiClient):
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def chat(self, system_msg: str, prompt: str, contexts:list=[]) -> str:
        
        ai_request = []

        if contexts:
            ai_request = [{"role": "system", "content": system_msg}] + contexts + [ {"role": "user", "content": prompt}]
        else:
            ai_request = [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ]
        
        response = self.client.chat.completions.create(
            model = self.model,
            messages = ai_request,
            temperature = self.temperature,
        )
        return response.choices[0].message.content.strip()
