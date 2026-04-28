from dataclasses import dataclass
from datetime import datetime

@dataclass
class Incident:
    id: str
    title: str
    description: str
    priority: str
    status: str
    source: str  # JIRA or SERVICENOW
    created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url: str = ""
    
    def to_dict(self):
        return self.__dict__