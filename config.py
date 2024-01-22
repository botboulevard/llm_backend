from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    
    LLM_URL = os.environ.get('LLM_URL_WITHOUT_TRAILING_SLASH',None)
    if LLM_URL is None:
        raise Exception("LLM_URL_WITHOUT_TRAILING_SLASH is not set")
    
    RUN_POD_ACCESS_TOKEN = os.environ.get('RUN_POD_ACCESS_TOKEN',None)
    if RUN_POD_ACCESS_TOKEN is None:
        raise Exception("RUN_POD_ACCESS_TOKEN is not set")
    
    ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN',None)
    if ACCESS_TOKEN is None:
        raise Exception("GITHUB_ACCESS_TOKEN is not set")