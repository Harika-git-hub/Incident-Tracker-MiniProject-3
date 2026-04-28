import pysnow
import config
from models.incident import Incident

class ServiceNowService:
    def __init__(self):
        config.validate()
        instance = config.SNOW_URL.replace("https://", "").replace(".service-now.com", "")
        self.client = pysnow.Client(instance=instance, user=config.SNOW_USER, password=config.SNOW_PASS)
        self.incident_table = self.client.resource(api_path=f'/table/{config.SNOW_TABLE}')
        print("✅ ServiceNow connected")

    def create_incident(self, title, description, priority="2"):
        # priority: 1=High, 2=Medium, 3=Low
        priority_map = {"High": "1", "Medium": "2", "Low": "3"}
        prio = priority_map.get(priority, "2")
        
        payload = {
            'short_description': title,
            'description': description,
            'urgency': prio,
            'impact': prio,
            'state': '1'
        }
        result = self.incident_table.create(payload=payload)
        return Incident(
            id=result['number'],
            title=title,
            description=description,
            priority=priority,
            status="New",
            source="SERVICENOW",
            url=f"{config.SNOW_URL}/nav_to.do?uri=incident.do?sys_id={result['sys_id']}"
        )

    def fetch_incidents(self):
        response = self.incident_table.get(query={'active': True}, stream=True)
        incidents = []
        state_map = {"1": "New", "2": "In Progress", "6": "Resolved", "7": "Closed"}
        prio_map = {"1": "High", "2": "Medium", "3": "Low"}
        
        for record in response.all():
            incidents.append(Incident(
                id=record['number'],
                title=record['short_description'],
                description=record['description'],
                priority=prio_map.get(record['urgency'], "Medium"),
                status=state_map.get(record['state'], "New"),
                source="SERVICENOW",
                url=f"{config.SNOW_URL}/nav_to.do?uri=incident.do?sys_id={record['sys_id']}"
            ))
        return incidents