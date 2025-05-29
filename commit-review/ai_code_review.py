import os
import subprocess
from dotenv import load_dotenv
from openai import OpenAI
import sys
import io

# === 환경 설정 ===
load_dotenv()
client = OpenAI()


# === 최근 커밋 메시지 n개 ===
def get_recent_commit_messages(n=3):
    result = subprocess.run(["git", "log", f"-n{n}", "--pretty=format:%s"], capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip()


# === 현재 커밋 메시지 (pre-commit에서는 .git/COMMIT_MESSAGE_TMP 사용) ===
def get_current_commit_message():
    try:
        with open(".git/COMMIT_EDITMSG", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


# === 현재 스테이지된 코드 변경 사항 ===
def get_staged_diff():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, encoding="utf-8")
    return result.stdout.strip()


# === 프롬프트 생성 ===
def build_prompt(recent_commits, current_commit, diff):
    system_msg = "너는 경험 많은 코드 리뷰어야. 주어진 커밋 메시지와 코드 변경을 바탕으로 리뷰를 제공해야 해."
    prompt = f"""최근 커밋 메시지는 다음과 같아:
{recent_commits}

현재 커밋 메시지는 다음과 같아:
{current_commit or '[현재 메시지가 없음]'}

그리고 현재 스테이지된 코드 변경(diff)은 다음과 같아:
{diff}

다음 내용을 수행해줘:
1. 커밋 메시지가 명확한지 판단하고, 더 나은 메시지가 있다면 제안해줘.
2. 코드 변경 사항의 품질을 평가하고, 개선 사항이나 버그 가능성을 리뷰해줘."""
    return system_msg, prompt


# === OpenAI API 호출 ===
def call_openai(system_msg, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# === 메인 함수 ===
def main():
    recent_commits = get_recent_commit_messages()
    current_commit = get_current_commit_message()
    diff = get_staged_diff()

    system_msg, prompt = build_prompt(recent_commits, current_commit, diff)
    result = call_openai(system_msg, prompt)

    print("\n [OpenAI 응답 결과]")
    print(result)
    return 1 # 0 반환 시 커밋 중단


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    main()
