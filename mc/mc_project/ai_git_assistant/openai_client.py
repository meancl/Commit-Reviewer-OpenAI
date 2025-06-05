from ai_git_assistant.ai_client import AiClient

class OpenAiClient(AiClient):
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature

    def chat(self, system_msg: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model= self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
        )
        return response.choices[0].message.content.strip()
