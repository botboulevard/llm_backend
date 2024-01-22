import logging
import os

# Create a logs folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure the logger for FastAPI
fastapi_logger = logging.getLogger("fastapi_logger")
fastapi_logger.setLevel(logging.DEBUG)

fastapi_handler = logging.FileHandler("logs/fastapi.log")
fastapi_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fastapi_handler.setFormatter(fastapi_formatter)

fastapi_logger.addHandler(fastapi_handler)

# Configure the logger for LLM
llm_logger = logging.getLogger("llm_logger")
llm_logger.setLevel(logging.DEBUG)

llm_handler = logging.FileHandler("logs/llm.log")
llm_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
llm_handler.setFormatter(llm_formatter)

llm_logger.addHandler(llm_handler)
