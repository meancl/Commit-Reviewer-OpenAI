import json
from pathlib import Path

LOG_FILE = Path("chat_log.json")

def save_context_message(role: str, content: str):
    """메시지를 로그파일에 누적 저장 (파일이 비어있거나 깨져 있어도 안전하게 처리)"""
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content_raw = f.read().strip()
                messages = json.loads(content_raw) if content_raw else []
        except json.JSONDecodeError:
            messages = []
    else:
        messages = []

    messages.append({
        "role": role,
        "content": content.strip()
    })

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)



def load_context_messages(limit:int=None) -> list:
    """
    저장된 메시지를 로드하여 리스트로 반환한다.
    - 파일이 없거나 비어 있는 경우 빈 리스트([])를 반환한다.
    - limit이 지정되면 최근 limit 쌍(user + assistant) 기준으로 최대 2 * limit개의 메시지를 반환한다.
    - limit이 None이면 전체 메시지를 반환한다.
    """
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                messages = json.loads(content)
                return messages if limit is None else messages[-limit * 2:]
        except json.JSONDecodeError:
            return []
    else:
        return []
    
    
    
    
    

    