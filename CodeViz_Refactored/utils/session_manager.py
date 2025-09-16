import json
import os
from datetime import datetime

SESSION_FILE = "session_data.json"

def load_session_data():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_session_data(start_time):
    session_data = load_session_data()
    
    end_time = datetime.now()
    duration = end_time - start_time

    new_entry = {
        "date": start_time.strftime("%Y-%m-%d"),
        "start": start_time.strftime("%H:%M:%S"),
        "end": end_time.strftime("%H:%M:%S"),
        "duration": str(duration).split(".")[0],
    }

    if "history" not in session_data:
        session_data["history"] = []

    session_data["history"].append(new_entry)
    
    # Keep only last 10 sessions
    session_data["history"] = session_data["history"][-10:]

    # Update additional metadata
    session_data["last_used"] = new_entry["date"]
    session_data["last_duration"] = new_entry["duration"]
    session_data["total_sessions"] = session_data.get("total_sessions", 0) + 1

    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f, indent=4)
