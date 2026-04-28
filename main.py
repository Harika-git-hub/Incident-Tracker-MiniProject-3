from services.jira import JiraService
from services.servicenow import ServiceNowService
from models.report import ReportGenerator
from utils.helpers import ensure_dirs, init_json_file
from utils.classifier import classify_priority
import config

def main():
    print("🚨 Starting Incident Tracker")
    ensure_dirs()
    init_json_file(config.DATA_PATH)
    
    jira = JiraService()
    snow = ServiceNowService()
    report = ReportGenerator()
    
    # Example: Create incident in both systems
    title = "Database connection timeout"
    description = "Production DB is timing out. Users cannot login."
    priority = classify_priority(title + " " + description)
    
    print(f"\nCreating incident with priority: {priority}")
    
    # Create in Jira
    jira_inc = jira.create_incident(title, description, priority)
    report.save_incident(jira_inc)
    print(f"Jira: {jira_inc.id} - {jira_inc.url}")
    
    # Create in ServiceNow
    snow_inc = snow.create_incident(title, description, priority)
    report.save_incident(snow_inc)
    print(f"ServiceNow: {snow_inc.id} - {snow_inc.url}")
    
    # Generate report
    report.generate_html_report()
    print(f"\n✅ Done. Check {config.REPORT_PATH}")
    
    # Fetch and display all
    print("\n=== JIRA INCIDENTS ===")
    for inc in jira.fetch_incidents()[:3]:
        print(f"{inc.id}: {inc.title} | {inc.status}")
    
    print("\n=== SERVICENOW INCIDENTS ===")
    for inc in snow.fetch_incidents()[:3]:
        print(f"{inc.id}: {inc.title} | {inc.status}")

if __name__ == "__main__":
    main()