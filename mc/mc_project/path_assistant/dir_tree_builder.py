from pathlib import Path
import os

def get_directory_structure_tree(root: Path , include_hidden: bool) -> str:
    """
    지정된 루트 디렉토리부터 시작해서 전체 디렉토리 구조를 트리 형태로 반환.
    숨김 파일(.git 등) 포함 여부는 include_hidden으로 제어.
    """
    result_lines = ["[ 디렉토리 구조 요약 ]", f"{root.name}/"]

    def walk(current_path: Path, prefix: str = ""):
        try:
            entries = os.listdir(current_path)
        except PermissionError:
            return  

        if not include_hidden:
            entries = [e for e in entries if not e.startswith(".")]

        entries = sorted(entries, key=lambda name: (not (current_path / name).is_dir(), name.lower()))
        count = len(entries)

        for idx, name in enumerate(entries):
            full_path = current_path / name
            connector = "└── " if idx == count - 1 else "├── "
            result_lines.append(f"{prefix}{connector}{name}")

            if full_path.is_dir():
                extension = "    " if idx == count - 1 else "│   "
                walk(full_path, prefix + extension)

    walk(root)
    return "\n".join(result_lines)
