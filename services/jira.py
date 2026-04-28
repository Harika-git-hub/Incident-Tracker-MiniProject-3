import os
from jira import JIRA

class JiraService:
    def __init__(self):
        self.jira = JIRA(
            server=os.getenv('JIRA_URL'),
            basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_TOKEN'))
        )
    
    def create_incident(self, title, description, priority):
        issue_dict = {
            'project': {'key': 'KAN'},
            'summary': title,
            'description': description,
            'issuetype': {'name': 'Task'},
            'priority': {'name': priority}
        }
        issue = self.jira.create_issue(fields=issue_dict)
        return {
            'id': issue.key,
            'url': f"{os.getenv('JIRA_URL')}/browse/{issue.key}",
            'system': 'Jira',
            'title': title,
            'priority': priority
        }