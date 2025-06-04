import argparse

import sys, io

from ai_git_assistant.prompt_builder import build_prompt
from ai_git_assistant.system_messages import init_openai_system_message
from ai_git_assistant.openai_client import call_openai
from ui_assistant.spinner_utils import Spinner

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8') 

def main():
    parser = argparse.ArgumentParser(prog="mc", description="AI 기반 Git 코드 리뷰")
    parser.add_argument("--mode", type=str, default="commit_message_and_review",
        choices=["commit_message_and_review", "commit_message", "commit_review", "directory_analyzer", "log_summarize", "git_question", "general"])
    parser.add_argument("--log", type=int, nargs='?', const=3, help="로그 갯수")
    parser.add_argument("--show", type=str, nargs='?', const='HEAD', help= "commit id")
    parser.add_argument("--diff", type=str, nargs='?', const="--cached")
    parser.add_argument("--file", type=str, help="파일 경로")
    parser.add_argument("--directory", action="store_true", help="디렉터리 구조")
    parser.add_argument("--request_confirm", action="store_true", help="AI 요청 메시지 확인")
    parser.add_argument("--include_hidden", action="store_true", help="숨김 파일 포함 여부")
    parser.add_argument("message", type=str, default="", nargs='?')

    args = parser.parse_args()  

    spinner = Spinner()
    display_contents = ""
    try:
        spinner.start()

        system_msg = init_openai_system_message()[args.mode]
        prompt = build_prompt(args)
        
        if args.request_confirm: 
            display_contents += f"[ **system message** ]\n{system_msg}\n\n[ **prompt message** ]\n{prompt}" 
        else:
            result = call_openai(system_msg, prompt)
            display_contents += f"\n[OpenAI 응답 결과]\n\n{result}"
    except Exception:
        print("\n오류로 인해 프로그램 중단")
    finally:
        spinner.stop()
        print(display_contents)

    return 0

if __name__ == "__main__":
    main()
