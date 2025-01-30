import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Sample dataset of alerts
data = {
    "message": [
        "Server down in US-East region",
        "Database connection timeout",
        "High CPU usage detected",
        "Service restarted successfully",
        "Network unreachable",
        "Disk space running low",
        "Memory leak detected",
        "Backup completed successfully",
        "Failed login attempt detected",
        "Application crash reported"
    ],
    "severity": [
        "Critical",
        "Warning",
        "Warning",
        "Info",
        "Critical",
        "Warning",
        "Critical",
        "Info",
        "Warning",
        "Critical"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Train the model
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

pipeline.fit(df["message"], df["severity"])

# Save the model
with open("alert_classifier.pkl", "wb") as model_file:
    pickle.dump(pipeline, model_file)

print("Model trained and saved!")