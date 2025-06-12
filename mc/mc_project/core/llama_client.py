from core.ai_client import AiClient

class LlamaClient(AiClient):
    def __init__(self, model: str = "meta-llama/Llama-4-Scout-17B-16E-Instruct", temperature: float = 0.3):
        from together import Together
        from dotenv import load_dotenv
        load_dotenv()
        self.client = Together()
        self.model = model
        self.temperature = temperature


    def chat(self, system_msg: str, prompt: str, contexts: list = [], stream: bool = True) -> str:
        
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
            stream = stream
        )

        if stream:
            result = ""
            for chunk in response:
                if len(chunk.choices) > 0 :
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    result += content
              
            print() 
            return result.strip()
        else:
            return response.choices[0].message.content.strip()


