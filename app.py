import logging
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from models import GitHubIssueSummarizerRequest
from util import extract_github_info
from LLM_helper import LLMHelper
import uvicorn
import time

# Configure allowed origins for CORS
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "https://github.com",
]

# Configure logging to a file
logging.basicConfig(filename="app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Processed request in {elapsed_time} seconds")
        return results

    except Exception as e:
        logger.error(f"Error in github_issue_summarizer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9876, workers=1)
