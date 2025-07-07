from flask import Flask, request, jsonify
import requests
import json  # <- wichtig für das Parsen von Strings zu JSON

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to your Copilot server!",
        "status": "ok"
    })

@app.route("/copilot", methods=["POST"])
def copilot():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # ↓↓↓ NEU: Den Prompt-String in ein echtes JSON-Objekt umwandeln
        payload = json.loads(prompt)
    except Exception as e:
        return jsonify({"error": "Invalid JSON in prompt", "details": str(e)}), 400

    gpt_webhook = "https://script.google.com/macros/s/AKfycbyRQ5gUisrZJKdJNoN_PixPrRIFJK0iTVBCoOOVVFkIMVcsyLzwWhg3Ch6dH4PdJt9n/exec"
    headers = {
        "Authorization": "Bearer 8235",
        "Content-Type": "application/json"
    }

    try:
        gpt_response = requests.post(gpt_webhook, json=payload, headers=headers)
        response_json = gpt_response.json()
    except Exception as e:
        return jsonify({"error": "Error contacting GPT service", "details": str(e)}), 502

    return jsonify({"response": response_json})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
