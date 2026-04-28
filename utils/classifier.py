def classify_priority(text):
    text = text.lower()
    if any(word in text for word in ['down', 'critical', 'outage', 'production', 'urgent']):
        return "High"
    elif any(word in text for word in ['slow', 'error', 'bug']):
        return "Medium"
    else:
        return "Low"