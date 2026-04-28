# Azure Boards disabled. Using Jira + ServiceNow only.
class AzureService:
    def __init__(self):
        print("⚠️  Azure Boards not configured")
    
    def create_incident(self, *args):
        raise NotImplementedError("Azure disabled")