from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import GitHubIssueSummarizerRequest
from util import extract_github_info
from llm_helper import LLMHelper
import uvicorn
import time
import os
from custom_logger import fastapi_logger

# Configure allowed origins for CORS
origins = [
    "https://github.com",
]

# Create FastAPI app
app = FastAPI()
llm = LLMHelper()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summarize/github_issue")
async def github_issue_summarizer(request: GitHubIssueSummarizerRequest):
    """
    Endpoint to summarize GitHub issues.

    Args:
        request (GitHubIssueSummarizerRequest): Request payload containing GitHub issue information.

    Returns:
        dict: Summarized response.
    """
    try:
        start_time = time.time()
        org, repo, issue_number = extract_github_info(request.url)
        results = llm.llm_response(repo_owner=org, issue_number=issue_number, repo_name=repo)
        end_time = time.time()
        elapsed_time = end_time - start_time
        fastapi_logger.info(f"Processed request in {elapsed_time} seconds")
        return results

    except Exception as e:
        fastapi_logger.error(f"Error in github_issue_summarizer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# @app.middleware("http")
# async def forward_to_localhost(request, call_next):
#     """
#     Middleware to forward requests to localhost:3000 for paths other than /summarize/github_issue.
#     """
#     if request.url.path != "/summarize/github_issue":
#         # Forward the request to localhost:3000
#         response = await request.httpx_client.get(llm_url + request.url.path)
#         # Return the response from localhost:3000
#         return response

#     return await call_next(request)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9876, workers=1)
