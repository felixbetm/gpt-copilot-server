from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Startseite zum Testen, ob Server läuft
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to your Copilot server!",
        "status": "ok"
    })

# API-Endpunkt für /copilot
@app.route("/copilot", methods=["POST"])
def copilot():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # Aktuelle Google Script URL + Token im Header
    gpt_webhook = "https://script.google.com/macros/s/AKfycbyRQ5gUisrZJKdJNoN_PixPrRIFJK0iTVBCoOOVVFkIMVcsyLzwWhg3Ch6dH4PdJt9n/exec"
    headers = {
        "Authorization": "Bearer 8235",
        "Content-Type": "application/json"
    }

    try:
        gpt_response = requests.post(gpt_webhook, json={"prompt": prompt}, headers=headers)
        response_json = gpt_response.json()
    except Exception as e:
        return jsonify({
            "error": "Error contacting GPT service",
            "details": str(e)
        }), 502

    return jsonify({"response": response_json})

# Start der App auf Port 10000 (für Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
