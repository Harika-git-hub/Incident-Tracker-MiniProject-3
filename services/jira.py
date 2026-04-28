from jira import JIRA
import config
from models.incident import Incident

class JiraService:
    def __init__(self):
        config.validate()
        self.jira = JIRA(
            server=config.JIRA_URL,
            basic_auth=(config.JIRA_EMAIL, config.JIRA_TOKEN)
        )
        print("✅ Jira connected")

    def create_incident(self, title, description, priority="Medium"):
        issue_dict = {
            'project': {'key': config.JIRA_PROJECT_KEY},
            'summary': title,
            'description': description,
            'issuetype': {'name': 'Bug'},
            'priority': {'name': priority}
        }
        issue = self.jira.create_issue(fields=issue_dict)
        return Incident(
            id=issue.key,
            title=title,
            description=description,
            priority=priority,
            status=issue.fields.status.name,
            source="JIRA",
            url=issue.permalink()
        )

    def fetch_incidents(self):
        jql = f'project = {config.JIRA_PROJECT_KEY} ORDER BY created DESC'
        issues = self.jira.search_issues(jql, maxResults=50)
        incidents = []
        for issue in issues:
            incidents.append(Incident(
                id=issue.key,
                title=issue.fields.summary,
                description=issue.fields.description or "",
                priority=issue.fields.priority.name,
                status=issue.fields.status.name,
                source="JIRA",
                url=issue.permalink()
            ))
        return incidents