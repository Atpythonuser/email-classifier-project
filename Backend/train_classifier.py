import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# ✅ Load CSV from data folder
data = pd.read_csv('./data/emails.csv')

X = data['text']
y = data['labels']

# ✅ Create vectorizer
vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(X)

# ✅ Train-Test split
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# ✅ Train Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ✅ Ensure model directory exists (optional)
os.makedirs('.', exist_ok=True)

# ✅ Save model & vectorizer directly in Backend folder
model = joblib.load("email_classifier.pkl")
vectorizer = joblib.load("vectorizer.pkl")


print("✅ Model and vectorizer saved successfully.")