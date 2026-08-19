from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or {}

    try:
        num1 = float(data["num1"])
        num2 = float(data["num2"])
        operation = data["operation"]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "num1, num2 and a valid operation are required"}), 400

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        result = num1 / num2
    else:
        return jsonify({"error": "Unsupported operation"}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
