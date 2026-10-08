from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

CORS(app)

AI_SERVICE_URL = os.getenv(
    "AI_SERVICE_URL",
    "http://localhost:5001"
)


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "Backend API"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data or "error" not in data:
        return jsonify({
            "error": "Please provide an error message."
        }), 400

    try:

        response = requests.post(
            "http://ai-service:5001/analyze",
            json={
                "error": data["error"]
            },
            timeout=10
        )

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as error:

        return jsonify({
            "error": "AI service is unavailable.",
            "details": str(error)
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)