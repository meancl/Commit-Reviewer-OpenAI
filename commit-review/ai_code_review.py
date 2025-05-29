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
    system_msg ="""\
    너는 숙련된 Git 코드 리뷰어로서, 다음 정보를 바탕으로 리뷰를 제공해야 해.
    - 커밋 메시지 품질 분석 및 개선 제안
    - 코드 변경(diff)의 품질 평가 및 개선점 또는 위험 요소 피드백 제공
    - 모든 응답은 **일반 텍스트 형식**으로 제공 (마크다운 금지)
    - 기본 언어는 **한글**이며, 커밋 메시지가 영어일 경우 영어로도 제안해줘
    - 출력은 **항목별로 간결하고 명확하게 정리**해줘
    """
    prompt = f"""\
    [최근 커밋 메시지들]
    {recent_commits}

    [현재 커밋 메시지]
    {current_commit or '[현재 메시지가 없음]'}

    [코드 변경 내용(diff)]
    {diff}

    [리뷰 요청]
    1. 코드 변경 사항의 품질을 평가하고, 문제점이나 개선할 부분이 있으면 알려줘.
    2. 현재 커밋 메시지가 적절한지 판단하고, 더 나은 메시지가 있다면 제안해줘.
    3. 메시지는 간결하고 실용적으로 제시해줘 (예: "feat: 사용자 로그인 기능 추가").
    """
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
    
    sys.exit(1) # 0 -> 커밋 진행 


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    main()
