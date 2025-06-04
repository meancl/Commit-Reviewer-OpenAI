import subprocess

def get_recent_commit_messages(n: int) -> str:
    if n == -1:
        cmd = ["git", "log", "--pretty=format:%s"]
    else:
        cmd = ["git", "log", f"-n{n}", "--pretty=format:%s"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    messages = result.stdout.strip().splitlines()
    return "[ git recent logs ]\n" + "\n".join(f"{msg}" for msg in messages)

def get_diff(diff_message: str) -> str:
    result = subprocess.run(["git", "diff", diff_message], capture_output=True, text=True, encoding="utf-8")
    messages = result.stdout.strip().splitlines()
    return "[ git diff ]\n" + "\n".join(f"{msg}" for msg in messages)

def get_commit_show(commit_id:   str) -> str:
    result = subprocess.run(["git", "show", commit_id], capture_output=True, text=True, encoding="utf-8")
    messages = result.stdout.strip().splitlines()
    return "[ git commit contents ]\n" + "\n".join(f"{msg}" for msg in messages)