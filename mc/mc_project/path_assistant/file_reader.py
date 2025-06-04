from pathlib import Path

def get_files_content(file_arg: str) -> str:
    result = []
    paths = file_arg.strip().split()
    idx = 0 
    for path_str in paths:
        path = Path(path_str)
        idx += 1
        if path.is_file():
            with path.open(encoding="utf-8") as f:
                content = f.read()
            result.append(f"[ file{idx}. {path.name} ]\n{content}\n")
        else:
            result.append(f"[ file{idx}. {path.name} ]\n<파일을 찾을 수 없습니다>\n")
    return "\n".join(result)