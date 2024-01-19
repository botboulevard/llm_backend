import time
import re

def timeit_wrapper(func):
    """
    A decorator that measures the execution time of a function.

    Args:
        func: The function to be decorated.

    Returns:
        function: The decorated function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.5f} seconds")
        return result

    return wrapper

def extract_github_info(url):
    """
    Extract GitHub information (organization, repository, issue number) from a GitHub issue URL.

    Args:
        url (str): GitHub issue URL.

    Returns:
        tuple: A tuple containing organization, repository, and issue number.
        
    Raises:
        ValueError: If the URL is not a valid GitHub issue URL.
    """
    # Define a regular expression pattern for GitHub issue URLs
    pattern = r'https://github\.com/([^/]+)/([^/]+)/issues/(\d+)'

    # Use re.match to find matches in the URL
    match = re.match(pattern, url)

    if match:
        org, repo, issue_number = match.groups()
        issue_number = int(issue_number)
        return org, repo, issue_number
    else:
        raise ValueError("Invalid GitHub issue URL")
