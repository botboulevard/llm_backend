from pydantic import BaseModel, Field
from typing import List
# from langchain_core.pydantic_v1 import BaseModel, Field


class GitHubIssueSummarizerRequest(BaseModel):
    url:str = Field(description="GitHub URL")


class CondensedComment(BaseModel):
    author: str
    comment: str


class CondensedIssue(BaseModel):
    title: str
    description: str
    comments: List[CondensedComment]

