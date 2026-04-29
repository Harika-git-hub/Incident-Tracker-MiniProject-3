# Incident Tracker Mini Project 3

Sync and track incidents between Jira and ServiceNow. This tool fetches Jira issues and creates/updates corresponding incidents in ServiceNow, keeping both systems in sync.

## Features
- **Bidirectional sync**: Jira Issues ↔ ServiceNow Incidents
- **Secure config**: Uses environment variables, no hardcoded secrets
- **Filtering**: Sync by Jira project, status, or custom JQL
- **Logging**: Track all API calls and errors
- **Python 3.8+**: Built with `requests` and `python-dotenv`

## Prerequisites
1. **Python 3.8+** installed
2. **ServiceNow Developer Instance**: Get one at https://developer.servicenow.com
3. **Jira Cloud Account** with API token: Generate at https://id.atlassian.com/manage-profile/security/api-tokens
4. **Git** for version control

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Harika-git-hub/Incident-Tracker-MiniProject-3.git
cd Incident-Tracker-MiniProject-3