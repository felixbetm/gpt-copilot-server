from flask import Flask, request, jsonify
import requests

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

    # Token wird direkt in die URL als Parameter eingebaut
    token = "8235"
    gpt_webhook = f"https://script.google.com/macros/s/AKfycbyRQ5gUisrZJKdJNoN_PixPrRIFJK0iTVBCoOOVVFkIMVcsyLzwWhg3Ch6dH4PdJt9n/exec?token={token}"

    try:
        gpt_response = requests.post(gpt_webhook, json={"prompt": prompt})
        response_json = gpt_response.json()
    except Exception as e:
        return jsonify({
            "error": "Error contacting GPT service",
            "details": str(e)
        }), 502

    return jsonify({"response": response_json})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
