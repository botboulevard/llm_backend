# from langchain_community.llms import vllm
# from langchain.prompts import PromptTemplate
# os.environ['CUDA_VISIBLE_DEVICES'] = "3"
# from vllm.model_executor.parallel_utils.parallel_state import destroy_model_parallel


# from langchain_community.llms import VLLM

import requests
import json
from github_issue import get_issue_details, transform_github_issue
from util import timeit_wrapper
# import os
from custom_logger import llm_logger
from typing import List

from pydantic import BaseModel
from config import Config

class TextSummary(BaseModel):
    input_tokens: int
    output_tokens: int
    text: List[str]

class OutputInfo(BaseModel):
    delayTime: int
    executionTime: int
    id: str
    output: TextSummary
    status: str

class RunPodAPIModel(BaseModel):
    delayTime: int
    executionTime: int
    id: str
    output: TextSummary
    status: str






class LLMHelper:
    def __init__(self):
        self.llm_url = Config.LLM_URL
        self.RUN_POD_ACCESS_TOKEN = Config.RUN_POD_ACCESS_TOKEN
        
        # self.base_url = f"{self.llm_url}/v1"
        
#         # destroy_model_parallel()
#         self.llm = VLLM(model="mistralai/Mistral-7B-Instruct-v0.2",
#            trust_remote_code=True,
#            max_new_tokens=128,
#            top_k=10,
#            top_p=0.95,
#            temperature=0.1,
#            # tensor_parallel_size=... # for distributed inference
# )
        
    
    @timeit_wrapper
    def _generate_prompt(self, title, description, comments):
        return f"""
                Below is a Github issue and its comments.
                
                Github Issue Title: {title}
                Github Issue Description: {description}
                Github Issue Comments: {comments}
                Based on this summarize the issue in 3 sections with 2 bullet points:
                
                1) What is the issue talking about
                2) what is the current status
                3) What help is given or needed
                
                
                Give me the output in markdown format
                """

    @timeit_wrapper
    def llm_response(self, issue_number: int, repo_name: str, repo_owner: str) -> RunPodAPIModel or None:
        try:
            llm_logger.info(f"Requesting LLM response for issue {issue_number} in repo {repo_name} owned by {repo_owner}")
            transformed_issue = transform_github_issue(get_issue_details(
                issue_number=issue_number,
                repo_name=repo_name,
                repo_owner=repo_owner
            ))
            
            data = {
                    "input": {
                        "prompt": self._generate_prompt(transformed_issue.title, transformed_issue.description, transformed_issue.comments),
                        "sampling_params":{
                             "max_new_tokens":128,
                                "top_k":10,
                                "top_p":0.95,
                                "temperature":0.1
                        }
                    }
                }
            
            llm_logger.info(f"Data sent to LLM: {str(data)}")
            
            # post_data = {
            #     "model": "mistralai/Mistral-7B-Instruct-v0.2",
            #     "messages":[
            #         {
            #             "role":"user",
            #             "content":self._generate_prompt(transformed_issue.title, transformed_issue.description, transformed_issue.comments),
            #         }
            #     ],
            #     # "prompt": self._generate_prompt(transformed_issue.title, transformed_issue.description, transformed_issue.comments),
            #     # "max_new_tokens": 128,
            #     "temperature": 0.1,
            #     # "top_k": 10,
            # }

            # headers = {'Content-Type': 'application/json'}
            
            headers = {'Content-Type': 'application/json','Authorization':f"""Bearer {self.RUN_POD_ACCESS_TOKEN}"""}
            
            # url = self.base_url + '/chat/completions'
            # response = requests.post(url, headers=headers, data=json.dumps(post_data))
            response = requests.post(self.llm_url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raises HTTPError for bad responses
            llm_logger.info(f"LLM response: {response.json()}")
            return_data = response.json()
            return return_data

        except requests.exceptions.RequestException as e:
            # Handle exceptions here
            print(f"Error during request: {e}")
            llm_logger.error(f"Error during request: {e}")
            return None  # Or raise an exception, log, or handle it as appropriate
        
        
        # return self.llm(self._generate_prompt(title, description, comments))
    
