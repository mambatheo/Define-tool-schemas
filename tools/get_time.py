from datetime import datetime

def get_time(location):
    return f"Current time in {location}: {datetime.now().strftime('%H:%M:%S')}"
