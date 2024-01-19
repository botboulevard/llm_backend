import time
import re

def timeit_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.5f} seconds")
        return result

    return wrapper


def extract_github_info(url):
    # Define a regular expression pattern for GitHub issue URLs
    pattern = r'https://github\.com/([^/]+)/([^/]+)/issues/(\d+)'

    # Use re.match to find matches in the URL
    match = re.match(pattern, url)

    if match:
        org = match.group(1)
        repo = match.group(2)
        issue_number = int(match.group(3))
        return org, repo, issue_number
    else:
        raise ValueError("Invalid GitHub issue URL")