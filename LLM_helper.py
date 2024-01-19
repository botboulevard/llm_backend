from langchain.llms import VLLM
from langchain.prompts import PromptTemplate



class LLMHelper:
    def __init__(self):
        self.llm = VLLM(model="mistralai/Mistral-7B-Instruct-v0.2",
           trust_remote_code=True,  # mandatory for hf models
           max_new_tokens=128,
           top_k=10,
           top_p=0.95,
           temperature=0.1,
           # tensor_parallel_size=... # for distributed inference
)


    def _generate_prompt(self, title, description, comments):
        return f"""
                Below is a Github issue and its comments.
                
                Github Issue Title: {title}
                Github Issue Description: {description}
                Github Issue Comments: {comments}
                Based on this summarize the issue in 3 sections:
                
                1) What is the issue talking about
                2) what is the current status
                3) What help is given or needed
                """

    
    def llm_response(self, title, description, comments):
        return self.llm(self._generate_prompt(title, description, comments))