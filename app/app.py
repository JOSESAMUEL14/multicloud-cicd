from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    cloud = os.getenv("CLOUD_PROVIDER", "local")
    return f"<h1>Hello from {cloud}!</h1><p>Multi-cloud CI/CD pipeline v2 - Automated with GitHub Actions!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
