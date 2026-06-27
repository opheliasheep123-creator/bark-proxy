from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BARK_TOKEN = "FVNwzXqaVYFCmaQaV8mvJd"
BARK_URL = f"https://api.day.app/{BARK_TOKEN}"

@app.route("/push", methods=["POST", "GET"])
def push():
    if request.method == "GET":
        title = request.args.get("title", "知臨")
        body = request.args.get("body", "")
    else:
        data = request.json or {}
        title = data.get("title", "知臨")
        body = data.get("body", "")
    
    url = f"{BARK_URL}/{title}/{body}"
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route("/", methods=["GET"])
def health():
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
