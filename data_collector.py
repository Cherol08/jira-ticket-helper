from utils import get_config
import pandas as pd
from jira import JIRA
from dotenv import load_dotenv
import os, requests
import jira
import base64


def fetch_jira_tickets():
    """Fetches Jira tickets using credentials from .env."""
    config = get_config()
    jira = JIRA(server=config['jira_url'], basic_auth=(config['jira_email'], config['api_key']))
    issues = jira.search_issues(f'project={config["project_key"]}', maxResults=60)
    
    data = []
    for issue in issues:
        comments = issue.fields.comment.comments
        # Prepare comment string with all comment bodies concatenated
        comment_bodies = "\n\n ".join([comment.body for comment in comments]) if comments else "No comments"
        # print(f"""key: {issue.key}
        #       \nsummary: {issue.fields.summary}
        #       \nassignee: {issue.fields.assignee}
        #       \ndescription: {issue.fields.description}
        #       \nstatus: {issue.fields.status.name}
        #       \ncreated: {issue.fields.created}
        #       \nresolved: {issue.fields.resolutiondate}
        #       \ncomments: {comment_bodies}  
        #       """             
        #     )
        data.append({
            'key': issue.key,
            'summary': issue.fields.summary,
            'assignee': issue.fields.assignee,
            'description': issue.fields.description,
            'status': issue.fields.status.name,
            'created': issue.fields.created,
            'resolved': issue.fields.resolutiondate,
            'comments': comment_bodies
        })
    return pd.DataFrame(data)


# def fetch_project_issues():
#     config = get_config()
#     headers = {
#         "Authorization": f"Basic {requests.auth._basic_auth_str(config['jira_email'], config['api_key'])}",
#         "Content-Type": "application/json"
#     }
#     url = f"{config['jira_url']}/rest/api/2/search"
#     payload = {"jql": f"project={config['project_key']}", "maxResults": 50}
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()  # Raises an exception for HTTP errors
#         issues = response.json()

#         data = []
#         for issue in issues:
#             comments = issue.fields.comment.comments
#             # Prepare comment string with all comment bodies concatenated
#             comment_bodies = " | ".join([comment.body for comment in comments]) if comments else "No comments"
#             print(f"""
#                 key: {issue.key}\n
#                 summary: {issue.fields.summary}\n
#                 assignee: {issue.fields.assignee}\n
#                 description: {issue.fields.description}\n
#                 status: {issue.fields.status.name}\n
#                 created: {issue.fields.created}\n
#                 resolved: {issue.fields.resolutiondate}\n
#                 comments: {comment_bodies}  
#                 """             
#             )
#             data.append({
#                 'key': issue.key,
#                 'summary': issue.fields.summary,
#                 'assignee': issue.fields.assignee,
#                 'description': issue.fields.description,
#                 'status': issue.fields.status.name,
#                 'created': issue.fields.created,
#                 'resolved': issue.fields.resolutiondate,
#                 'comments': comment_bodies
                
                
#             })
#         return pd.DataFrame(data)
#     except requests.exceptions.HTTPError as err:
#         print(f"HTTP error occurred: {err}")
#     except requests.exceptions.RequestException as err:
#         print(f"Error occurred: {err}")
#     return None


# def fetch_projects():
#     config = get_config()
#     """Fetch all Jira projects accessible to the user."""
#     url = f"{config['jira_url']}/rest/api/3/project/"
#     response = requests.get(
#         url, 
#         auth=(config['jira_email'], config['api_key']), 
#         headers={"Accept": "application/json"}
#     )
    
#     if response.status_code == 200:
#         projects = response.json()
#         if projects:
#             print("Projects retrieved:")
#             for project in projects:
#                 print(f"{project['key']}: {project['name']}")
#         else:
#             print("No projects found.")
#     else:
#         print(f"Failed to fetch projects. Status code: {response.status_code}")
#         print(f"Response: {response.text}")



issues = fetch_jira_tickets()
print(issues,)
# fetch_projects()