from fastapi import HTTPException
import requests
from models import CondensedComment, CondensedIssue
from util import timeit_wrapper
import os

# Load environment variables from .env file

# Retrieve GitHub access token from environment variables
ACCESS_TOKEN = os.environ.get('GITHUB_ACCESS_TOKEN')

@timeit_wrapper
def transform_github_issue(issue):
    """
    Transform GitHub issue data into a condensed format.

    Args:
        issue (dict): Raw GitHub issue data.

    Returns:
        CondensedIssue: Condensed representation of the GitHub issue.
    """
    title = issue['title']
    description = issue['body']
    comments = []

    for comment in issue['comments']['nodes']:
        author = comment['author']['login']
        comments.append(CondensedComment(author=author, comment=comment['body']))

    return CondensedIssue(title=title, description=description, comments=comments)

@timeit_wrapper
def get_issue_details(issue_number: int, repo_name: str, repo_owner: str):
    """
    Retrieve details of a GitHub issue.

    Args:
        issue_number (int): Issue number.
        repo_name (str): Name of the repository.
        repo_owner (str): Owner of the repository.

    Returns:
        dict: Raw GitHub issue data.
    """
    print("Request Received 1")
    
    # Validate request parameters
    if not issue_number or not repo_name or not repo_owner:
        raise HTTPException(status_code=400, detail="Invalid request parameters")

    # Check if GitHub access token is set
    if not ACCESS_TOKEN:
        raise HTTPException(status_code=500, detail="GitHub access token not set")

    # GitHub API headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # GitHub GraphQL query
    query = f"""query {{
        repository(owner: "{repo_owner}", name: "{repo_name}") {{
            issue(number: {issue_number}) {{
                title
                body
                comments(first: 20) {{
                    nodes {{
                        author {{
                            login
                        }}
                        body
                    }}
                }}
            }}
        }}
    }}"""

    url = 'https://api.github.com/graphql'

    try:
        # Make GitHub API request
        response = requests.post(url, headers=headers, json={'query': query})
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse response JSON
        issue_data = response.json()
        issue_instance = issue_data['data']['repository']['issue']
        return issue_instance

    except requests.exceptions.RequestException as e:
        # Handle request-related errors
        raise HTTPException(status_code=500, detail=f"GitHub API request failed: {str(e)}")

    except KeyError as e:
        # Handle missing key in response JSON
        raise HTTPException(status_code=500, detail=f"Failed to parse GitHub API response: {str(e)}")
