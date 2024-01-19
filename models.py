from typing import List
from pydantic import BaseModel, Field
# from langchain_core.pydantic_v1 import BaseModel, Field


class GitHubIssueSummarizerRequest(BaseModel):
    issue: int = Field(description="Issue number")
    org: str = Field(description="Organization name")
    repo: str = Field(description="Repository name")    
    
from typing import List, Optional
from pydantic import BaseModel

from pydantic import BaseModel, Field

class GitHubAuthor(BaseModel):
    login: str

class GitHubComment(BaseModel):
    author: GitHubAuthor
    body: str

class GitHubIssue(BaseModel):
    title: str
    body: str
    comments: list[GitHubComment]




class CondensedComment(BaseModel):
    author: str
    comment: str


class CondensedIssue(BaseModel):
    title: str
    description: str
    comments: list[
       CondensedComment
    ]

