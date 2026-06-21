# src/diff_parser.py
from git import Repo

def get_staged_diff():
    repo = Repo(".")
    # Gets the diff of staged changes
    return repo.git.diff("--staged")