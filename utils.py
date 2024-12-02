from dotenv import load_dotenv
import os, requests
import jira
# Load environment variables
load_dotenv()

def get_config():
    """Reads configuration values from .env file."""
    return {
        'jira_url': os.getenv('JIRA_URL'),
        'jira_email': os.getenv('USER_EMAIL'),
        'username': os.getenv('JIRA_USERNAME'),
        'api_key': os.getenv('JIRA_API_KEY'),
        'project_key': os.getenv('JIRA_PROJECT_KEY'),
        'openai_api_key': os.getenv('OPENAI_API_KEY')
    }



# def fetch_project_issues():
#     config = get_config()
#     url = f"{config['jira_url']}/rest/api/3/issue/TTSD-3055"
#     # payload = {"jql": f"project = {config['project_key']}", "maxResults": 50}
#     # try:
#     print(url)
#     response = requests.get(url,
#                             auth=(config['jira_email'], config['api_key']),
#                             headers={"Accept": "application/json"})
#     # response.raise_for_status()  # Raises an exception for HTTP errors
#     if response.status_code == 200:
#         return response.json()
#     # except requests.exceptions.HTTPError as err:
#     #     print(f"HTTP error occurred: {err}")
#     # except requests.exceptions.RequestException as err:
#     #     print(f"Error occurred: {err}")
#     return None

# # Debug: Check project key being used
# # print(f"Using project key: {config['project_key']}")
# issues = fetch_project_issues()

# if issues:
#     print(issues)
# else:
#     print("No issues found or an error occurred.")
    
# https://geointafrica.atlassian.net/rest/api/3/issue/TTSD-3055
# https://geointafrica.atlassian.net/rest/api/3/issue/TTSD-3055