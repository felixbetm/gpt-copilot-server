from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Copilot-Server läuft!",
        "status": "ok"
    })

@app.route("/copilot", methods=["POST"])
def copilot():
    # Einfaches BTC-Wachstumsbeispiel, +15% jährlich (monatlich aufgeteilt)
    sheet_name = "api-test"
    range_str = "A1:B13"
    values = [["Monat", "BTC-Preis (15% p.a.)"]]

    startwert = 40000
    for monat in range(1, 13):
        wachstumsfaktor = (1 + 0.15) ** (monat / 12)
        preis = round(startwert * wachstumsfaktor, 2)
        values.append([f"Monat {monat}", preis])

    # Google Script Webhook
    gpt_webhook = "https://script.google.com/macros/s/AKfycbyRQ5gUisrZJKdJNoN_PixPrRIFJK0iTVBCoOOVVFkIMVcsyLzwWhg3Ch6dH4PdJt9n/exec"
    headers = {
        "Authorization": "Bearer 8235",
        "Content-Type": "application/json"
    }

    payload = {
        "sheet": sheet_name,
        "range": range_str,
        "values": values
    }

    try:
        response = requests.post(gpt_webhook, json=payload, headers=headers)
        return jsonify({"response": response.json()})
    except Exception as e:
        return jsonify({
            "error": "Fehler beim Senden an Google Apps Script",
            "details": str(e)
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
