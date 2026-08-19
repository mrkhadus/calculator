from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    backend_url = "http://localhost:5001"
    return render_template("index.html", backend_url=backend_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
