# Git Commit AI Reviewer

AI 기반 커밋 메시지 및 코드 리뷰 자동화 도구입니다.  
OpenAI GPT 모델을 활용하여 Git 커밋 시점에 커밋 메시지와 스테이지된 코드 변경 사항을 분석하고, 품질 향상을 위한 리뷰를 제공합니다.

## 폴더 구조
your-project-root/
├── .git/                  # Git 저장소 폴더  
├── .gitignore             # Git 무시 파일 설정  
├── .githooks/  
│   └── ai_code_review.py  # AI 기반 코드 리뷰 스크립트  
├── commit-review/  
│   └── setup.sh           # Git Hook 등록 자동화 스크립트  
│   └── requirements.txt   # 필요 Python 패키지 목록  
├── .env                   # 환경변수 파일  
└── README.md             

## 설치 방법
1. OpenAI API 키를 발급받아 준비합니다.
2. `.git` 폴더와 같은 위치에 `commit-review` 폴더 전체를 복사합니다.
3. 터미널에서 아래 명령어로 설치 스크립트를 실행합니다

```bash
cd commit-review
./setup.sh
```

4.루트 경로에 .env 파일을 생성하고 다음 내용을 입력합니다.
```
OPENAI_API_KEY=sk-입력한_API_키
```
## 기능 설명
### git hooks
커밋 메시지를 읽어 AI에게 전달하고, 더 나은 메시지를 제안받습니다.
최근 커밋 히스토리 및 현재 변경 사항을 함께 전송합니다.
메시지가 부족하거나 명확하지 않을 경우 AI가 개선안을 출력합니다.

```bash
git add .
git commit -m "기능 추가"
```
→ AI가 커밋 메시지에 대한 피드백과 코드 리뷰를 출력해줍니다.

커밋 훅을 생략하고 싶을 때
커밋 시 아래처럼 --no-verify 옵션을 주면 훅이 실행되지 않습니다.

```bash
git commit -m "메시지" --no-verify
```

설치가 다 된 후 commit-review 디렉터리를 삭제해도 좋습니다.
