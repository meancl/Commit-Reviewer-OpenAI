import os
from pathlib import Path

def find_git_directory(start_path: Path = Path.cwd()) -> Path | None:
    """
    현재 디렉토리에서 시작해서 상위로 올라가며 .git 디렉토리를 찾는다.
    찾으면 해당 경로(Path)를 반환하고, 없으면 None 반환.
    """
    current = start_path.resolve()

    for parent in [current] + list(current.parents):
        if (parent / ".git").is_dir():
            return parent
    return None

def change_to_git_root() -> Path:
    """
    .git 디렉토리가 존재하는 최상위 디렉토리로 이동하고 그 경로를 반환한다.
    """
    git_root = find_git_directory()
    if not git_root:
        raise FileNotFoundError(".git 디렉토리를 찾을 수 없습니다.")
    
    os.chdir(git_root)
    return git_root

def find_cur_directory() -> Path:
    return Path.cwd()
