from git_utils.git_commands import get_diff, get_commit_show, get_recent_commit_messages
from git_utils.git_project_finder import find_cur_directory, find_git_directory
from fs.tree_builder import get_directory_structure_tree
from fs.file_loader import get_files_content

def append_prompt_message(args) -> str:
    prompt_messages = []
    if args.diff:
        prompt_messages.append(get_diff(args.diff))
    if args.show:
        prompt_messages.append(get_commit_show(args.show))
    if args.log:
        prompt_messages.append(get_recent_commit_messages(args.log))
    if args.file:
        prompt_messages.append(get_files_content(args.file))
    if args.directory:
        include_hidden = False
        if args.include_hidden:
            include_hidden = True
        root = find_cur_directory()
        prompt_messages.append(get_directory_structure_tree(root, include_hidden=include_hidden))

    return "\n\n".join(prompt_messages)

def build_prompt(args) -> str:
    if args.message:
        prompt = f"[ user message ]\n{args.message}\n\n"
    else:
        prompt = ""

    if args.mode in {"commit_message", "commit_message_and_review"}:
        if not args.diff:
            args.diff = "--cached"
    if args.mode == "commit_review":
        if not (args.diff or args.show):
            raise ValueError("commit_review 모드에서는 --diff 또는 --show 중 하나는 필수입니다.")
    if args.mode in {"git_question", "general"}:
        if not args.message:
            raise ValueError("git_question 모드에서는 message 필수입니다.")
    if args.mode == 'directory_analyzer':
        if not args.directory:
            args.directory = True
    git_dir = find_git_directory()
    need_git = args.diff or args.show or args.log
    if git_dir is None and need_git:
        raise FileNotFoundError("이 디렉토리에서 .git 디렉토리를 찾을 수 없습니다.")
    
    prompt += append_prompt_message(args)
    return prompt

