import os
from dotenv import load_dotenv

load_dotenv()

# JIRA
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL") 
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")

# SERVICENOW
SNOW_URL = os.getenv("SERVICENOW_URL")
SNOW_USER = os.getenv("SERVICENOW_USER")
SNOW_PASS = os.getenv("SERVICENOW_PASS")
SNOW_TABLE = "incident"

# PATHS
DATA_PATH = "data/incident.json"
REPORT_PATH = "output/report.html"

def validate():
    required = [JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, SNOW_URL, SNOW_USER, SNOW_PASS]
    if not all(required):
        raise ValueError("Missing credentials in .env file")
    print("✅ Config validated")