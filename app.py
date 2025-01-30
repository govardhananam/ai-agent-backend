from fastapi import FastAPI
import pickle
import sqlite3
from .models import Message
app = FastAPI()

# Connect to the SQLite database
conn = sqlite3.connect("alerts.db")
cursor = conn.cursor()

app = FastAPI()

# Load the trained AI model
with open("alert_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.post("/receive_alert/")
def receive_alert(alert: Message):
    severity = model.predict([alert.message])[0]  # AI predicts severity
    status = "Acknowledged" if severity == "Info" else "Escalated"

    # Store in DB
    cursor.execute("INSERT INTO alerts (message, severity, status) VALUES (?, ?, ?)", 
                   (alert.message, severity, status))
    conn.commit()

    action = {
        "Critical": "Restarting affected service...",
        "Warning": "Notifying on-call engineer...",
        "Info": "Logging alert, no action required."
    }.get(severity, "No action taken.")

    return {
        "alert_received": alert.message,
        "severity": severity,
        "status": status,
        "action_taken": action
    }

@app.get("/alerts/")
def get_alerts():
    cursor.execute("SELECT * FROM alerts")
    data = cursor.fetchall()
    return {"alerts": data}
