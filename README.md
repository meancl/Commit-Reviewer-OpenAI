# Git Commit AI Reviewer

AI 기반 커밋 메시지 및 코드 리뷰 자동화 도구입니다.  
LLM 모델을 활용하여 Git 커밋 시점에 커밋 메시지와 스테이지된 코드 변경 사항을 분석하고, 품질 향상을 위한 리뷰를 제공합니다.

## 폴더 구조
```
McProject/
├── mc
│   ├── mc_project
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── ai_client.py
│   │   │   ├── ai_client_provider.py
│   │   │   ├── gemini_client.py
│   │   │   ├── llama_client.py
│   │   │   ├── openai_client.py
│   │   │   ├── prompt_builder.py
│   │   │   └── system_messages.py
│   │   ├── fs
│   │   │   ├── __init__.py
│   │   │   ├── context_manager.py
│   │   │   ├── file_loader.py
│   │   │   └── tree_builder.py
│   │   ├── git_utils
│   │   │   ├── __init__.py
│   │   │   ├── git_commands.py
│   │   │   └── git_project_finder.py
│   │   ├── ui
│   │   │   ├── __init__.py
│   │   │   └── spinner.py
│   │   └── main.py
│   ├── mc
│   ├── requirements.txt
│   └── setup.sh
├── LICENSE
└── README.md

```  

## 설치 방법
1. OpenAI API 키를 발급받아 준비합니다.
2. 터미널에서 아래 명령어로 설치 스크립트를 실행합니다
   *(현재는 Git Bash 환경에 최적화된 Shell 스크립트만 제공됩니다.)*

```bash
./setup.sh
```

3. 사용자 경로에  '.global-bin/.env' 파일에 다음 내용을 입력합니다.
```
OPENAI_API_KEY=api_key_here
...
...
```

## 명령어 사용법
### 기본 실행
```bash
git add .
mc
```

## 주요 옵션 정리
| 옵션                        | 설명                                                  |
|---------------------------|-----------------------------------------------------|
| -m, --mode                | 실행 모드 (아래 참조)                                 |
| -l, --log                 | Git 로그 개수 지정                                    |
| -s, --show                | git show 옵션 지정                                   |
| -d, --diff                | git diff 옵션 지정                                   |
| -f, --file                | 파일 경로 입력                                       |
| -D, --directory           | 디렉토리 트리 구조 표시                              |
| -r, --request_confirm     | AI 프롬프트 확인 메시지 표시                         |
| -H, --include_hidden      | 숨김 파일 포함 여부                                  |
| -c, --include_context     | 과거 대화 context 포함 (기본: 전체, 숫자 입력 시 최근 N쌍) |
| -x, --exclude_save_context | 결과 context 저장하지 않음                          |
| -M, --model | llm 모델 지정                          |
| -S, --exclude_stream | stream print 제외                          |
        
## 모드 요약 (--mode 또는 -m)
| 단축키 | 전체 명칭                 | 설명                         |
|--------|--------------------------|------------------------------|
| cmr    | commit_message_and_review | 커밋 메시지 + 코드 리뷰 생성 |
| cm     | commit_message            | 커밋 메시지만 생성           |
| cr     | commit_review             | 코드 리뷰만 생성             |
| da     | directory_analyzer        | 디렉토리 구조 분석           |
| ls     | log_summarize             | 커밋 로그 요약               |
| gq     | git_question              | Git 관련 질문 응답           |
| gen    | general                   | 일반 질문 응답               |

## 모델 설명
| 옵션           | 설명                                                                                               |
|----------------|----------------------------------------------------------------------------------------------------|
| model_provider | 사용할 AI 모델 제공자를 지정합니다. 가능한 값: `openai`, `gemini`, `llama`                         |
| model_name     | 사용할 모델의 정확한 이름을 지정합니다. 기본값은 각 provider에 따라 다릅니다:                    |
|                | - `openai`  → `gpt-4o-mini`                                                                         |
|                | - `gemini`  → `gemini-1.5-flash`                                                                    |
|                | - `llama`   → `meta-llama/Llama-4-Scout-17B-16E-Instruct`                                           |


```bash
# 예시
mc -m cmr --log 5
```

## 설치 후 디렉터리 정리
설치가 완료되면 mc 디렉터리는 삭제해도 무방합니다.
필요한 실행 파일 및 설정은 .global-bin에 위치합니다.
