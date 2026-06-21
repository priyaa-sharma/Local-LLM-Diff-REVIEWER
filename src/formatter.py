# src/formatter.py
from .models import ReviewResult

def print_review(result: ReviewResult):
    print(f"\n--- Review Summary ---\n{result.summary}\n")
    if not result.comments:
        print("No issues found!")
    for comment in result.comments:
        print(f"[{comment.severity.upper()}] {comment.file_name} (Line {comment.line_number}): {comment.comment}")