#!/bin/bash
set -e

echo "커밋 리뷰 환경 설정을 시작합니다..."

LOCAL_ROOT=$(pwd)                       # /your-project-root/commit-review
PROJECT_ROOT=$(dirname "$LOCAL_ROOT") # /your-project-root

if [ -f "$PROJECT_ROOT/.gitignore" ]; then
    echo "" >> "$PROJECT_ROOT/.gitignore"
    cat "$LOCAL_ROOT/.gitignore" >> "$PROJECT_ROOT/.gitignore"
    rm -f "$LOCAL_ROOT/.gitignore"
    echo ".gitignore를 덧붙여 썻습니다."
else
    mv -f "$LOCAL_ROOT/.gitignore" "$PROJECT_ROOT/.gitignore"
    echo ".gitignore를 이동했습니다."
fi

mkdir -p "$PROJECT_ROOT/.githooks"
echo ".githooks 디렉토리를 생성했습니다."

mv -f "$LOCAL_ROOT/ai_code_review.py" "$PROJECT_ROOT/.githooks/ai_code_review.py"
echo "ai_code_review.py를 .githooks로 이동했습니다."

mv -f "$LOCAL_ROOT/commit-msg" "$PROJECT_ROOT/.git/hooks/commit-msg"
mv -f "$LOCAL_ROOT/post-commit" "$PROJECT_ROOT/.git/hooks/post-commit"
chmod +x "$PROJECT_ROOT/.git/hooks/commit-msg"
chmod +x "$PROJECT_ROOT/.git/hooks/post-commit"
echo "commit-msg, post-commit 훅을 이동하고 실행 권한을 부여했습니다."


if [ ! -d "$PROJECT_ROOT/.venv" ]; then
  echo "Python 가상환경 생성 중..."
  python3 -m venv "$PROJECT_ROOT/.venv"
fi

source "$PROJECT_ROOT/.venv/Scripts/activate"
echo "requirements.txt로 패키지 설치 중..."
pip install -r "$LOCAL_ROOT/requirements.txt"
rm -f "$LOCAL_ROOT/requirements.txt"

if [ ! -f "$PROJECT_ROOT/.env" ]; then
  echo ".env 파일 생성 중..."
  echo "OPENAI_API_KEY=여기에_본인의_API_KEY를_입력하세요" > "$PROJECT_ROOT/.env"
  echo ".env 파일을 열어 OPENAI_API_KEY 값을 반드시 설정하세요!"
fi

echo -e "\n커밋 리뷰 환경이 성공적으로 설정되었습니다."
echo "커밋 시 AI가 메시지와 코드를 자동으로 리뷰합니다."