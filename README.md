# Git Commit AI Reviewer

AI 기반 커밋 메시지 및 코드 리뷰 자동화 도구입니다.  
OpenAI GPT 모델을 활용하여 Git 커밋 시점에 커밋 메시지와 스테이지된 코드 변경 사항을 분석하고, 품질 향상을 위한 리뷰를 제공합니다.

## 폴더 구조
mc_project
├── ai_git_assistant
│   ├── dir_tree_builder.py
│   ├── git_project_finder.py
│   ├── git_utils.py
│   ├── openai_client.py
│   ├── prompt_builder.py
│   └── system_messages.py
├── ui_assistant
│   └── spinner_utils.py
├── main.py
└── .gitignore

## 설치 방법
1. OpenAI API 키를 발급받아 준비합니다.
2. 터미널에서 아래 명령어로 설치 스크립트를 실행합니다

```bash
./setup.sh
```

3.사용자 경로에  '.global-bin/.env' 파일에 다음 내용을 입력합니다.
```
OPENAI_API_KEY=sk-입력한_API_키
```
## 기능 설명

## 모드별 사용법 (`mc --mode`)
| 모드명                      | 역할 설명 |
|----------------------------|------------|
| commit_message_and_review | 메시지 + 코드 리뷰 생성 |
| commit_message             | 커밋 메시지만 생성 |
| commit_review              | 코드 리뷰만 생성 |
| directory_analyzer         | 디렉토리 구조 분석 |
| log_summarize              | 커밋 로그 요약 분석 |
| git_question               | Git 관련 질문 대응 |

```bash
git add .
mc # default: --mode commit_message_and_review --diff
```
→ AI가 커밋 메시지에 대한 피드백과 코드 리뷰를 출력해줍니다.

설치가 다 된 후 mc 디렉터리를 삭제해도 좋습니다.
