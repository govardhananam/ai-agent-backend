from fastapi import FastAPI, Query
import pickle
import sqlite3
from models import Message
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "https://ai-alert-frontend.vercel.app"
]

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect("alerts.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Load the trained AI model
with open("alert_classifier.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.post("/receive_alert/")
def receive_alert(alert: Message):
    print(alert.message)
    severity = model.predict([alert.message])[0]  # AI predicts severity
    print(severity)
    status = "Acknowledged" if severity == "Info" else "Escalated"

    conn = get_db_connection()
    cursor = conn.cursor()
    # Store in DB
    cursor.execute("INSERT INTO alerts (message, severity, status) VALUES (?, ?, ?)", 
                   (alert.message, severity, status))
    conn.commit()
    conn.close()

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

@app.get("/receive_alert/")
def receive_alert(message: str = Query(..., description="Alert message to process")):
    severity = model.predict([message])[0]  # AI predicts severity
    status = "Acknowledged" if severity == "Info" else "Escalated"

    conn = get_db_connection()
    cursor = conn.cursor()
    # Store in DB
    cursor.execute("INSERT INTO alerts (message, severity, status) VALUES (?, ?, ?)", 
                   (message, severity, status))
    conn.commit()
    conn.close()

    action = {
        "Critical": "Restarting affected service...",
        "Warning": "Notifying on-call engineer...",
        "Info": "Logging alert, no action required."
    }.get(severity, "No action taken.")

    return {
        "alert_received": message,
        "severity": severity,
        "status": status,
        "action_taken": action
    }

@app.get("/alerts/")
def get_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts")
    data = cursor.fetchall()
    conn.close()

    return {"alerts": data}
