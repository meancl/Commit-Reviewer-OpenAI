import os
from core.ai_client import AiClient
from PIL import Image


class GeminiClient(AiClient):
    def __init__(self, model: str = 'gemini-1.5-flash', temperature: float = 0.3):
        import google.generativeai as genai
        from dotenv import load_dotenv
        load_dotenv()
        self.API_KEY = os.getenv("GOOGLE_API_KEY")
        if not self.API_KEY:
            raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        self.genai = genai
        self.genai.configure(api_key=self.API_KEY)
        self.model_name = model
        self.temperature = temperature
        self.model = self.genai.GenerativeModel(self.model_name)

    def chat(self, system_msg: str, prompt: str, contexts: list = [], stream: bool = True, images=None) -> str:
        full_prompt = f"{system_msg}\n\n{prompt}"
        generation_config = self.genai.GenerationConfig(temperature=self.temperature)
        parts = [full_prompt]

        if images:
            image_paths = images.strip().split()
            for image_path in image_paths:
                if os.path.exists(image_path):
                    try:
                        img = Image.open(image_path)
                        parts.append(img)
                    except Exception as e:
                        print(f"[경고] 이미지 열기 실패: {image_path} - {e}")

        result = ""

        if contexts:
            contexts = self.convert_to_gemini_context(contexts)
            chat_session = self.model.start_chat(history=contexts)
            if stream:
                response_stream = chat_session.send_message(parts, generation_config=generation_config, stream=True)
            else:
                response = chat_session.send_message(parts, generation_config=generation_config)
                return response.text.strip()
        else:
            if stream:
                response_stream = self.model.generate_content(parts, generation_config=generation_config, stream=True)
            else:
                response = self.model.generate_content(parts, generation_config=generation_config)
                return response.text.strip()

        # 공통 stream 처리
        for chunk in response_stream:
            for part in chunk.parts:
                print(part.text, end="", flush=True)
                result += part.text

        return result.strip()

    def convert_to_gemini_context(self, messages: list) -> list:
        converted = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")

            if role == "assistant":
                role = "model"

            converted.append({
                "role": role,
                "parts": [content]
            })
        return converted
