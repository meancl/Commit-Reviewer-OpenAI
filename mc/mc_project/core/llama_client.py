from core.ai_client import AiClient
import base64
import os

class LlamaClient(AiClient):
    def __init__(self, model: str = "meta-llama/Llama-4-Scout-17B-16E-Instruct", temperature: float = 0.3):
        from together import Together
        from dotenv import load_dotenv
        load_dotenv()
        self.client = Together()
        self.model = model
        self.temperature = temperature

    def encode_image_to_data_url(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {path}")
        with open(path, "rb") as f:
            b = f.read()
        return f"data:image/png;base64,{base64.b64encode(b).decode('utf-8')}"

    def chat(self, system_msg: str, prompt: str, contexts: list = [], stream: bool = True, images: str = "") -> str:
        ai_request = []
        if contexts:
            ai_request = [{"role": "system", "content": system_msg}] + contexts
        else:
            ai_request = [{"role": "system", "content": system_msg}]

       
        user_content = [{"type": "text", "text": prompt}]

        if images:
            for image_path in images.strip().split():
                try:
                    data_url = self.encode_image_to_data_url(image_path)
                    user_content.append({
                        "type": "image_url",
                        "image_url": {"url": data_url}
                    })
                except FileNotFoundError as e:
                    print(f"[경고] 이미지 생략됨: {e}")

        ai_request.append({
            "role": "user",
            "content": user_content
        })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=ai_request,
            temperature=self.temperature,
            stream=stream
        )

        if stream:
            result = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    result += content
            print()
            return result.strip()
        else:
            return response.choices[0].message.content.strip()
