import logging
from fastapi import FastAPI
from fastapi import HTTPException
import os
from contextlib import asynccontextmanager
from LLM_helper import llm
from models import GitHubIssueSummarizerRequest


# logging.basicConfig(level=logging.INFO)
logger = logging.basicConfig(filename="object_detection_service.log",level=logging.INFO)
# Set up logging
# logging.basicConfig(filename="object_detection_service.log", level=logging.INFO)
import uvicorn
from LLM_helper import LLMHelper

app = FastAPI()
llm = LLMHelper()

import time

@app.post("/summarize/github_issue")
async def github_issue_summarizer(request: GitHubIssueSummarizerRequest):
    try:
        start = time.time()
        print("Request Received")
        
        print("Going to function")
        results = llm.llm_response(
            title=request.title,
            description=request.description,
            comments=request.comments
        )
        end = time.time()
        print(end - start) # Time in seconds, e.g. 5.38091952400282
        return results
    except Exception as e:
        logging.error(f"Error in code_helper_request: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9876,reload=True)
    
    
    
    # ssh -L 9876:0.0.0.0:9876 sfsu_me -N -v -v