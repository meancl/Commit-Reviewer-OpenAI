from core.ai_client import AiClient
import base64
import os

class OpenAiClient(AiClient):
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        self.client = OpenAI()
        self.model = model
        self.temperature = temperature
        

    def chat(self, system_msg: str, prompt: str, contexts:list=[], stream:bool=True, images=None) -> str:
        
        ai_request = []

        if contexts:
            ai_request = [{"role": "system", "content": system_msg}] + contexts
        else:
            ai_request = [{"role": "system", "content": system_msg}]
        
        user_content = [{"type": "text", "text": prompt}]

        def encode_image_to_base64(image_path: str) -> str:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
            
        if images:
            image_paths = images.strip().split()
            for image_path in image_paths:
                if os.path.exists(image_path):
                    base64_image = encode_image_to_base64(image_path)
                    user_content.append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    })

        ai_request.append({
                "role": "user",
                "content": user_content
            })
    
        response = self.client.chat.completions.create(
            model = self.model,
            messages = ai_request,
            temperature = self.temperature,
            stream = stream
        )

        if stream:
            result = ""
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end="", flush=True) 
                result += content
            print() 
            return result.strip()
        else:
            return response.choices[0].message.content.strip()
