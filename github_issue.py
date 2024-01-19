from fastapi import HTTPException
import requests
from models import CondensedComment, CondensedIssue, GitHubIssue

ACCESS_TOKEN =  "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"



def tranform_github_issue(issue)->CondensedIssue:
    title = issue['title']
    description = issue['body']
    comments = []
    
    for comment in issue['comments']['nodes']:
        author = comment['author']['login']
        comments.append(CondensedComment(author=author, comment=comment['body']))
    
    return CondensedIssue(title=title, description=description, comments=comments)
    
def get_issue_details(
    issue_number: int,
    repo_name: str,
    repo_owner: str)-> GitHubIssue:
    """
    Get issue details from GitHub
    """
    if not issue_number:
        raise HTTPException(status_code=400, detail="No issue number in the request")
    if not repo_name:
        raise HTTPException(status_code=400, detail="No repo name in the request")
    if not repo_owner:
        raise HTTPException(status_code=400, detail="No repo owner in the request")

    headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28"
    }
    
    query = f""" query {{
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
    }}
    """
    
    url = 'https://api.github.com/graphql'
    response = requests.post(url, headers=headers, json={'query': query})
    issue_data = response.json()
    issue_instance = GitHubIssue(**issue_data['data']['repository']['issue'])
    return issue_instance




