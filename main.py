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
    
    # LIST OF 30 INCIDENTS TO CREATE - 15 Critical, 9 High, 4 Medium, 2 Low
    incidents_to_create = [
        {"title": "Database connection timeout", "desc": "Production DB is timing out. Users cannot login.", "severity": "Critical", "type": "network", "team": "backend"},
        {"title": "API Gateway 503 Error", "desc": "All API requests failing with 503", "severity": "High", "type": "app", "team": "backend"},
        {"title": "Firewall rule blocking traffic", "desc": "External IPs cannot reach web servers", "severity": "High", "type": "network", "team": "infra"},
        {"title": "SSL Certificate Expired", "desc": "Website showing security warnings", "severity": "Critical", "type": "security", "team": "infra"},
        {"title": "High CPU on App Server", "desc": "Server-01 CPU at 95% for 30 mins", "severity": "Medium", "type": "app", "team": "backend"},
        {"title": "Disk space full on DB", "desc": "Only 2% disk left on mysql-prod", "severity": "High", "type": "network", "team": "infra"},
        {"title": "Payment gateway timeout Stripe API 503", "desc": "Checkout failing for customers", "severity": "Critical", "type": "app", "team": "backend"},
        {"title": "Ransomware signature detected on workstation", "desc": "Endpoint protection flagged file", "severity": "Critical", "type": "security", "team": "infra"},
        {"title": "DNS resolution intermittent on network", "desc": "Users report sites not loading", "severity": "High", "type": "network", "team": "infra"},
        {"title": "Scheduled job failed non-production", "desc": "Nightly ETL job failed at 2 AM", "severity": "Low", "type": "app", "team": "backend"},
        {"title": "Phishing email reported by employees", "desc": "Multiple users got fake login email", "severity": "Medium", "type": "security", "team": "infra"},
        {"title": "Intermittent packet loss on VLAN 30", "desc": "Network latency spikes every 5 mins", "severity": "High", "type": "network", "team": "infra"},
        {"title": "Checkout service returning NullPointerException", "desc": "Java exception in prod logs", "severity": "High", "type": "app", "team": "backend"},
        {"title": "Suspicious login attempts from unknown IP", "desc": "Multiple failed logins from Russia", "severity": "Medium", "type": "security", "team": "infra"},
        {"title": "Network switch offline in DC rack B", "desc": "Switch-05 unreachable, failover active", "severity": "Critical", "type": "network", "team": "infra"},
        {"title": "Production Database CLUSTER DOWN", "desc": "All DB nodes unreachable. Complete outage.", "severity": "Critical", "type": "network", "team": "backend"},
        {"title": "Data Center Power Failure Rack A", "desc": "UPS failed, 20+ servers offline", "severity": "Critical", "type": "network", "team": "infra"},
        {"title": "Ransomware Attack Detected Domain Controllers", "desc": "Encryption started on DC-01", "severity": "Critical", "type": "security", "team": "infra"},
        {"title": "Payment Gateway Complete Outage", "desc": "Zero transactions processing. Revenue loss $50k/hr", "severity": "Critical", "type": "app", "team": "backend"},
        {"title": "SSL Certificate Expired All Customer Domains", "desc": "All websites showing security warnings", "severity": "Critical", "type": "security", "team": "infra"},
        {"title": "Core Network Switch Stack Failure", "desc": "Primary switch stack crashed. Network down", "severity": "Critical", "type": "network", "team": "infra"},
        {"title": "Customer Data Breach Confirmed", "desc": "500K user records exposed via API", "severity": "Critical", "type": "security", "team": "backend"},
        {"title": "Kubernetes Cluster Master Nodes Down", "desc": "All prod workloads failing to schedule", "severity": "Critical", "type": "app", "team": "infra"},
        {"title": "SAN Storage Array Failed All Volumes Offline", "desc": "Production storage completely unavailable", "severity": "Critical", "type": "network", "team": "infra"},
        {"title": "Active Directory Forest Trust Broken", "desc": "Users cannot authenticate company-wide", "severity": "Critical", "type": "security", "team": "infra"},
        {"title": "API Gateway 503 Error Spike", "desc": "30% of requests failing with 503", "severity": "High", "type": "app", "team": "backend"},
        {"title": "Firewall rule blocking payment traffic", "desc": "External IPs cannot reach checkout", "severity": "High", "type": "network", "team": "infra"},
        {"title": "Disk space critical on DB 95% full", "desc": "Only 5% disk left on mysql-prod", "severity": "High", "type": "network", "team": "infra"},
        {"title": "High CPU on App Server Cluster", "desc": "Server-01 to 05 CPU at 90%", "severity": "Medium", "type": "app", "team": "backend"},
        {"title": "Phishing campaign targeting employees", "desc": "Multiple users got fake login email", "severity": "Medium", "type": "security", "team": "infra"},
    ]
    
    # LOOP AND CREATE ALL 30 INCIDENTS
    for idx, inc in enumerate(incidents_to_create, 1):
        print(f"\n--- [{idx}/30] Creating: {inc['title']} ---")
        
        priority = classify_priority(inc['title'] + " " + inc['desc'])
        
        # Jira
        jira_inc = jira.create_incident(inc['title'], inc['desc'], priority)
        jira_inc['severity'] = inc['severity']
        jira_inc['type'] = inc['type']
        jira_inc['team'] = inc['team']
        report.save_incident(jira_inc)
        print(f"Jira: {jira_inc['id']} - {jira_inc['url']}")
        
        # ServiceNow
        snow_inc_obj = snow.create_incident(inc['title'], inc['desc'], priority)
        snow_inc = {
            'id': snow_inc_obj.id,
            'title': snow_inc_obj.title,
            'status': snow_inc_obj.status,
            'url': snow_inc_obj.url,
            'severity': inc['severity'],
            'type': inc['type'],
            'team': inc['team']
        }
        report.save_incident(snow_inc)
        print(f"ServiceNow: {snow_inc['id']} - {snow_inc['url']}")
    
    report.generate()
    print(f"\n✅ Done. Total incidents: {len(report.incidents)}")
    print(f"✅ Report saved to: {config.REPORT_PATH}")
    
if __name__ == "__main__":
    main()