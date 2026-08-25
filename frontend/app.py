from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:5001")

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/calculate")
def calculate():
    """Proxy requests to backend"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/calculate",
            json=request.get_json(),
            timeout=5
        )
        return response.json(), response.status_code
    except (requests.RequestException, ValueError) as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
