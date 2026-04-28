import json
import pandas as pd
from datetime import datetime
import config

class ReportGenerator:
    def __init__(self):
        self.data_path = config.DATA_PATH
        self.report_path = config.REPORT_PATH
    
    def save_incident(self, incident):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        data.append(incident.to_dict())
        
        with open(self.data_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def generate_html_report(self):
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        except:
            data = []
            
        if not data:
            html = "<h1>No incidents found</h1>"
        else:
            df = pd.DataFrame(data)
            html = f"""
            <html>
            <head><title>Incident Report</title></head>
            <body>
                <h1>Incident Report - {datetime.now().strftime("%Y-%m-%d %H:%M")}</h1>
                <p>Total Incidents: {len(df)}</p>
                {df.to_html(index=False, escape=False)}
            </body>
            </html>
            """
        
        with open(self.report_path, 'w') as f:
            f.write(html)
        print(f"✅ Report generated: {self.report_path}")