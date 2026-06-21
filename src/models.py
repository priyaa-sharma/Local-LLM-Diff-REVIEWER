from pydantic import BaseModel
from typing import List

class ReviewComment(BaseModel):
    file_name: str
    line_number: int
    comment: str
    severity: str  # "info", "warning", "error"

class ReviewResult(BaseModel):
    summary: str
    comments: List[ReviewComment]