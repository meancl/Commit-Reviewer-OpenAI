#!/bin/bash

set -e

GLOBAL_BIN="$HOME/.global-bin"
ENV_FILE=".env"
SOURCE_DIR="./mc_project"
SOURCE_FILE="./mc"
LOCAL_ROOT=$(pwd)  

echo " ~/.global-bin 디렉토리 생성 중..."
mkdir -p "$GLOBAL_BIN"

if [ -d "$SOURCE_DIR" ]; then
    echo "mc_project 디렉토리를 ~/.global-bin으로 이동 중..."
    mv "$SOURCE_DIR" "$GLOBAL_BIN/"
else
    echo "mc_project 디렉토리가 현재 위치에 없습니다."
    exit 1
fi

if [ -f "$SOURCE_FILE" ]; then
	echo "mc 파일을 ~/.global-bin으로 이동 중..."
	mv "$SOURCE_FILE" "$GLOBAL_BIN/"
else
    echo "mc 파일이 현재 위치에 없습니다."
    exit 1
fi

echo ".env 파일 생성 중..."
cat <<EOF > "$GLOBAL_BIN/$ENV_FILE"
# 환경 변수는 여기에 정의하세요
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
EOF

pip install -r "$LOCAL_ROOT/requirements.txt"
rm -f "$LOCAL_ROOT/requirements.txt"


if ! grep -q "export PATH=\"$GLOBAL_BIN:\$PATH\"" ~/.bash_profile; then
  echo "export PATH=\"$GLOBAL_BIN:\$PATH\"" >> ~/.bash_profile
  echo "PATH 설정을 ~/.bash_profile에 추가했습니다"
else
  echo "PATH 설정이 이미 존재합니다"
fi

source ~/.bash_profile