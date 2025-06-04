from .git_utils import get_diff, get_commit_show, get_recent_commit_messages
from ai_git_assistant.git_project_finder import change_to_git_root, find_cur_directory
from ai_git_assistant.dir_tree_builder import get_directory_structure_tree

def append_prompt_message(args) -> str:
    prompt_messages = []
    if args.diff:
        prompt_messages.append(get_diff(args.diff))
    if args.show:
        prompt_messages.append(get_commit_show(args.show))
    if args.log:
        prompt_messages.append(get_recent_commit_messages(args.log))
    return "\n\n".join(prompt_messages)

def build_prompt(args) -> str:
    if args.message:
        prompt = f"[ ##message## ]\n{args.message}\n\n"
    else:
        prompt = ""

    if args.mode in {"commit_message", "commit_message_and_review"}:
        if not args.diff:
            args.diff = "--cached"
    if args.mode == "commit_review":
        if not (args.diff or args.show):
            raise ValueError("commit_review 모드에서는 --diff 또는 --show 중 하나는 필수입니다.")
    if args.mode == "git_question":
        if not args.message:
            raise ValueError("git_question 모드에서는 message 필수입니다.")
    if args.mode == 'directory_analyzer':
        include_hidden = False
        if args.include_hidden:
            include_hidden = True
        #root = change_to_git_root()
        root = find_cur_directory()
        prompt += get_directory_structure_tree(root, include_hidden=include_hidden)
        prompt += "\n\n"
    
    prompt += append_prompt_message(args)
    return prompt

