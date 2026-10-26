import subprocess
from pathlib import Path


def get_staged_diff(repo_path: str | Path | None = None) -> str:
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True,
        check=True,
        cwd=repo_path,
    )
    return result.stdout