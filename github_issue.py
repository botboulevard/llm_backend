from fastapi import HTTPException
import requests
from models import CondensedComment, CondensedIssue
from util import timeit_wrapper

ACCESS_TOKEN =  "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"


@timeit_wrapper
def transform_github_issue(issue)->CondensedIssue:
    title = issue['title']
    description = issue['body']
    comments = []
    
    for comment in issue['comments']['nodes']:
        author = comment['author']['login']
        comments.append(CondensedComment(author=author, comment=comment['body']))
    
    return CondensedIssue(title=title, description=description, comments=comments)

@timeit_wrapper    
def get_issue_details(issue_number: int, repo_name: str, repo_owner: str):
    print("Request Received 1")
    if not issue_number or not repo_name or not repo_owner:
        raise HTTPException(status_code=400, detail="Invalid request parameters")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

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
        response = requests.post(url, headers=headers, json={'query': query})
        issue_data = response.json()
        print(response)
        print(issue_data)
        issue_instance = issue_data['data']['repository']['issue']
        return issue_instance

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"GitHub API request failed: {str(e)}")



