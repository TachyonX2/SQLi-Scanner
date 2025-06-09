
from flask import Flask, render_template, request, jsonify
from scanner import scan_url
import os
from datetime import datetime

app = Flask(__name__)

SCAN_HISTORY = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            if not url.endswith("?id="):
                url += "?id="
            result = scan_url(url)
            SCAN_HISTORY.append({
                "url": url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "result": result
            })
    return render_template("index.html", result=result)

@app.route("/api/scan", methods=["POST"])
def api_scan():
    data = request.json
    url = data.get("url")
    if url:
        if not url.endswith("?id="):
            url += "?id="
        result = scan_url(url)
        return jsonify(result)
    return jsonify({"error": "URL not provided"}), 400

@app.route("/history")
def history():
    return render_template("history.html", history=SCAN_HISTORY)

if __name__ == "__main__":
    app.run(debug=True)
