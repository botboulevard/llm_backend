import logging
from fastapi import FastAPI
from fastapi import HTTPException
import os
from contextlib import asynccontextmanager
from models import GitHubIssueSummarizerRequest
from util import extract_github_info
from fastapi.middleware.cors import CORSMiddleware

# from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel
origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    "https://github.com",
]




# logging.basicConfig(level=logging.INFO)
logger = logging.basicConfig(filename="app.log",level=logging.INFO)
# Set up logging
# logging.basicConfig(filename="object_detection_service.log", level=logging.INFO)
import uvicorn
from LLM_helper import LLMHelper

app = FastAPI()
llm = LLMHelper()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import time

@app.post("/summarize/github_issue")
async def github_issue_summarizer(request: GitHubIssueSummarizerRequest):
    try:
        # print(request.issue)
        start = time.time()
        # print("Request Received")
        # https://github.com/vercel/next.js/issues/60363
        org, repo, issue_number = extract_github_info(request.url)
        # print("Going to function")
        results = llm.llm_response(
           repo_owner= org,
           issue_number=issue_number,
           repo_name=repo
        )
        end = time.time()
        print(end - start) # Time in seconds, e.g. 5.38091952400282
        return results
    except Exception as e:
        print(e)
        logging.error(f"Error in code_helper_request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9876,workers=1)
    
    
    
    # ssh -L 9876:0.0.0.0:9876 sfsu_me -N -v -v
    # uvicorn app:app --host 0.0.0.0 --port 3000 --reload