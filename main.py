from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to your Copilot server!", "status": "ok"})

@app.route("/copilot", methods=["POST"])
def copilot():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    # Beispiel: einfache Antwortlogik – später GPT-Integration möglich
    if prompt == "BTC_Preis":
        return jsonify({
            "status": "ok",
            "antwort": "Zielpreis 2045: 21.000.000 EUR – exponentielle Kurve"
        })
    else:
        return jsonify({"status": "error", "antwort": f"Unbekannter Prompt: {prompt}"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
