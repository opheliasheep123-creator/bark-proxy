from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

BARK_TOKEN = "FVNwzXqaVYFCmaQaV8mvJd"
BARK_URL = f"https://api.day.app/{BARK_TOKEN}"
ACCESS_TOKEN = "caelum-ophelia-2026"

def send_bark(title, body):
    url = f"{BARK_URL}/{title}/{body}"
    resp = requests.get(url)
    return resp.json()

@app.route("/push", methods=["POST", "GET"])
def push():
    if request.method == "GET":
        title = request.args.get("title", "知臨")
        body = request.args.get("body", "")
    else:
        data = request.json or {}
        title = data.get("title", "知臨")
        body = data.get("body", "")
    result = send_bark(title, body)
    return jsonify(result)

@app.route("/mcp", methods=["POST"])
def mcp():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ACCESS_TOKEN}":
        return jsonify({"error": "unauthorized"}), 401

    data = request.json
    method = data.get("method")

    if method == "initialize":
        return jsonify({
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "bark-proxy", "version": "1.0.0"}
        })

    if method == "tools/list":
        return jsonify({
            "tools": [{
                "name": "send_notification",
                "description": "發送Bark通知給Ophelia",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "通知標題"},
                        "body": {"type": "string", "description": "通知內容"}
                    },
                    "required": ["body"]
                }
            }]
        })

    if method == "tools/call":
        params = data.get("params", {})
        args = params.get("arguments", {})
        title = args.get("title", "知臨")
        body = args.get("body", "")
        result = send_bark(title, body)
        return jsonify({
            "content": [{"type": "text", "text": json.dumps(result)}]
        })

    return jsonify({"error": "unknown method"}), 400

@app.route("/", methods=["GET"])
def health():
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)from flask import Flask, request, jsonify
