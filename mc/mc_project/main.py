import argparse

import sys, io

from core import get_ai_provider, build_prompt, init_openai_system_message
from fs import save_context_message, load_context_messages
from ui.spinner import Spinner

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8') 

def main():

    MODE_MAP = {
    "cmr": "commit_message_and_review",
    "cm": "commit_message",
    "cr": "commit_review",
    "da": "directory_analyzer",
    "ls": "log_summarize",
    "gq": "git_question",
    "gen": "general"
    }
    parser = argparse.ArgumentParser(prog="mc", description="Git and General assisatnat by CLI",
                                     usage="mc [-m MODE] [options] [message]",
                                     epilog="예시: mc -m cmr --log 5"
                                     )
    parser.add_argument("-m", "--mode", type=str, choices=MODE_MAP.keys(), default="cmr", help="Mode: " + ", ".join([f"{k}({v})" for k, v in MODE_MAP.items()]))
    parser.add_argument("-l", "--log", type=int, nargs='?', const=3, help="log number")
    parser.add_argument("-s", "--show", type=str, nargs='?', const='HEAD', help= "show option")
    parser.add_argument("-d", "--diff", type=str, nargs='?', const="--cached", help="diff option")
    parser.add_argument("-f", "--file", type=str, help="file paths seperated by space")
    parser.add_argument("-i", "--image", type=str, default=None, help="image paths seperated by space")
    parser.add_argument("-D", "--directory", action="store_true", help="directory tree structure")
    parser.add_argument("-r", "--request_confirm", action="store_true", help="show ai request message for confirm")
    parser.add_argument("-H", "--include_hidden", action="store_true", help="including hidden files")
    parser.add_argument("-c", "--include_context", type=int, nargs='?', default=argparse.SUPPRESS, const=None, help="including context messages")
    parser.add_argument("-x", "--exclude_save_context", action="store_true", help="excluding saving context message")
    parser.add_argument("-M", "--model", type=str, default='openai', choices=["openai", "gemini", "llama"], help="setting ai model")
    parser.add_argument("-S", "--exclude_stream", action="store_true", help="make stream off")
    parser.add_argument("message", type=str, default="", nargs='?', help="message or question for ai")

    args = parser.parse_args()  
    args.mode = MODE_MAP[args.mode]
  
    spinner = Spinner()
    display_contents = ""
    try:
        spinner.start()

        system_msg = init_openai_system_message()[args.mode]
        prompt = build_prompt(args)

        if hasattr(args, "include_context"):
            contexts = load_context_messages(args.include_context)
        else:
            contexts = [] 

        if args.request_confirm: 
            display_contents += f"[ **system message** ]\n{system_msg}\n\n[ **prompt message** ]\n{prompt}" 
            if contexts:
                display_contents += f"\n\n[ **contexts** ]\n{contexts}"
            if args.image:
                image_paths = '\n'.join(args.image.strip().split())
                display_contents += f"\n[ **image_paths** ]\n{image_paths}"    
        else:
            client = get_ai_provider(args.model)
            if not args.exclude_stream: 
                spinner.stop() 
                print("[AI 응답 결과]\n\n")
                result = client.chat(system_msg, prompt, contexts=contexts, images=args.image)
            else:                
                result = client.chat(system_msg, prompt, contexts=contexts, stream=False, images=args.image)
                display_contents += f"\n[AI 응답 결과]\n\n{result}"

            if not args.exclude_save_context:
                save_context_message("user", prompt)
                save_context_message("assistant", result)
    except Exception as e:
        print(f"\n오류로 인해 프로그램 중단\n오류 메시지 : {e}")
    finally:
        spinner.stop()
        print(display_contents)

    return 0

if __name__ == "__main__":
    main()
