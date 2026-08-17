from pathlib import Path

import joblib
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
model = joblib.load(MODEL_DIR / "spam_classifier.pkl")

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or request.form
    subject = str(data.get("subject", "")).strip()
    body = str(data.get("body", "")).strip()

    if not subject and not body:
        return jsonify({"error": "Enter a subject or email body to analyze."}), 400

    text = f"Subject: {subject}\n\nBody: {body}"
    features = vectorizer.transform([text])
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities) * 100)

    return jsonify({
        "label": "SPAM" if prediction == 1 else "HAM",
        "confidence": round(confidence, 2),
        "message": (
            "This email contains patterns commonly associated with spam."
            if prediction == 1
            else "This email appears to be legitimate."
        ),
    })


if __name__ == "__main__":
    app.run(debug=True)
