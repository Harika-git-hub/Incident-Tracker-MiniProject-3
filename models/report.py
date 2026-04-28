import config
from datetime import datetime
from collections import Counter

class ReportGenerator:
    def __init__(self):
        self.incidents = []
    
    def save_incident(self, incident):
        """Add incident to report - KEEP severity/type/team from main.py"""
        # Convert to dict format
        if isinstance(incident, dict):
            inc_dict = {
                'id': incident['id'],
                'title': incident['title'],
                'severity': incident.get('severity', 'MEDIUM'),  # ← FIXED: Use passed value
                'type': incident.get('type', 'network'),          # ← FIXED: Use passed value
                'team': incident.get('team', 'backend'),          # ← FIXED: Use passed value
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'status': incident.get('status', 'To Do'),
                'jira_url': incident['url'] if 'KAN' in incident['id'] else None,
                'snow_url': incident['url'] if 'INC' in incident['id'] else None
            }
        else:
            inc_dict = {
                'id': incident.id,
                'title': incident.title,
                'severity': getattr(incident, 'severity', 'MEDIUM'),  # ← FIXED
                'type': getattr(incident, 'type', 'network'),         # ← FIXED
                'team': getattr(incident, 'team', 'backend'),         # ← FIXED
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'status': incident.status,
                'jira_url': incident.url if 'KAN' in incident.id else None,
                'snow_url': incident.url if 'INC' in incident.id else None
            }
        
        self.incidents.append(inc_dict)
        print(f"Added to report: {inc_dict['id']} - {inc_dict['severity']}")
    
    def generate(self):
        """Generate HTML dashboard report"""
        total = len(self.incidents)
        severity_counts = Counter([i['severity'] for i in self.incidents])
        critical = severity_counts.get('Critical', 0)  # ← FIXED: Match case from main.py
        high = severity_counts.get('High', 0)
        medium = severity_counts.get('Medium', 0)
        low = severity_counts.get('Low', 0)
        
        type_counts = Counter([i['type'] for i in self.incidents])
        team_counts = Counter([i['team'] for i in self.incidents])
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>IT Incident Auto-Triage Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #f5f7fa;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{ font-size: 24px; margin-bottom: 5px; }}
        .header .meta {{ font-size: 13px; opacity: 0.9; }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: #fff;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .card .number {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .card .label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .card.total {{ border-color: #1e3c72; }}
        .card.total .number {{ color: #1e3c72; }}
        .card.critical {{ border-color: #d32f2f; }}
        .card.critical .number {{ color: #d32f2f; }}
        .card.high {{ border-color: #f57c00; }}
        .card.high .number {{ color: #f57c00; }}
        .card.medium {{ border-color: #fbc02d; }}
        .card.medium .number {{ color: #fbc02d; }}
        
        .breakdown {{
            margin-bottom: 30px;
        }}
        .breakdown h3 {{
            font-size: 14px;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}
        .tags {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}
        .tag {{
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
        }}
        .tag.network {{ background: #e3f2fd; color: #1976d2; }}
        .tag.security {{ background: #fce4ec; color: #c2185b; }}
        .tag.app {{ background: #f3e5f5; color: #7b1fa2; }}
        .tag.infra {{ background: #e8f5e9; color: #388e3c; }}
        .tag.backend {{ background: #fff3e0; color: #f57c00; }}
        
        .severity-badge {{
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            display: inline-block;
        }}
        .severity-Critical {{ background: #ffcdd2; color: #c62828; }}  <!-- FIXED: Capital C -->
        .severity-High {{ background: #ffe0b2; color: #e65100; }}
        .severity-Medium {{ background: #fff9c4; color: #f57f17; }}
        .severity-Low {{ background: #c8e6c9; color: #2e7d32; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        th {{
            background: #1e3c72;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}
        tr:hover {{ background: #f5f5f5; }}
        .ticket-links a {{
            color: #1e3c72;
            text-decoration: none;
            margin-right: 8px;
            font-size: 11px;
        }}
        .ticket-links a:hover {{ text-decoration: underline; }}
        .id-cell {{ font-weight: 600; color: #1e3c72; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>IT Incident Auto-Triage Report</h1>
        <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Incidents: {total}</div>
    </div>
    <div class="container">
        <div class="summary">
            <div class="card total">
                <div class="number">{total}</div>
                <div class="label">Total Incidents</div>
            </div>
            <div class="card critical">
                <div class="number">{critical}</div>
                <div class="label">Critical</div>
            </div>
            <div class="card high">
                <div class="number">{high}</div>
                <div class="label">High</div>
            </div>
            <div class="card medium">
                <div class="number">{medium + low}</div>
                <div class="label">Medium/Low</div>
            </div>
        </div>
        
        <div class="breakdown">
            <h3>Breakdown by Type</h3>
            <div class="tags">
"""
        
        for type_name, count in type_counts.items():
            html += f'<span class="tag {type_name}">{type_name.upper()}: {count}</span>'
        
        html += """
            </div>
            <h3>Breakdown by Team</h3>
            <div class="tags">
"""
        
        for team_name, count in team_counts.items():
            html += f'<span class="tag {team_name}">{team_name.upper()}: {count}</span>'
        
        html += f"""
            </div>
        </div>
        
        <h3 style="margin-bottom: 15px; color: #666; text-transform: uppercase; font-size: 14px;">Incident Detail</h3>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Severity</th>
                    <th>Type</th>
                    <th>Team</th>
                    <th>Timestamp</th>
                    <th>Tickets</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for inc in self.incidents:
            jira_link = f'<a href="{inc["jira_url"]}" target="_blank">JIRA</a>' if inc.get('jira_url') else ''
            snow_link = f'<a href="{inc["snow_url"]}" target="_blank">SNOW</a>' if inc.get('snow_url') else ''
            
            html += f"""
                <tr>
                    <td class="id-cell">{inc['id']}</td>
                    <td>{inc['title']}</td>
                    <td><span class="severity-badge severity-{inc['severity']}">{inc['severity']}</span></td>
                    <td>{inc['type']}</td>
                    <td>{inc['team']}</td>
                    <td>{inc['timestamp']}</td>
                    <td class="ticket-links">{jira_link} {snow_link}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
    </div>
</body>
</html>"""
        
        with open(config.REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ Report saved to {config.REPORT_PATH}")