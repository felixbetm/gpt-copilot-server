from flask import Flask, request, jsonify
import requests, os, json

# --- Konfiguration -----------------------------------------------------------
SCRIPT_URL    = "https://script.google.com/macros/s/AKfycbx9Etr5D74F8R8YVL4xbc-zqzPm4ka6F08l_nKg1RHvCUAVYcWaaCo3I2Nab4bjmw8P/exec"
SECRET_TOKEN  = "8235"           # ggf. via os.getenv("SECRET_TOKEN")

app = Flask(__name__)

# --- Health-Check ------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Copilot-Server läuft."})

# --- Generische Write-Route --------------------------------------------------
@app.route("/write", methods=["POST"])
def write():
    """
    Erwartet JSON-Body:
    {
      "sheet":  "<Tabellenblatt-Name>",
      "range":  "<A1-Range>",
      "values": [[..],[..]]
    }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    payload = {
        "token":  SECRET_TOKEN,
        "sheet":  data.get("sheet"),
        "range":  data.get("range"),
        "values": data.get("values")
    }

    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return jsonify(r.json()), r.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": "Apps Script nicht erreichbar", "details": str(err)}), 502

# --- Beispiel-Route BTC-Tabelle ---------------------------------------------
@app.route("/btc-demo", methods=["POST"])
def btc_demo():
    startwert = 40000
    werte = [["Monat", "BTC-Preis (+15 % p.a.)"]]

    for m in range(1, 13):
        faktor = (1 + 0.15) ** (m / 12)
        preis  = round(startwert * faktor, 2)
        werte.append([f"Monat {m}", preis])

    payload = {
        "token":  SECRET_TOKEN,
        "sheet":  "api-test",
        "range":  "A1:B13",
        "values": werte
    }
    try:
        r = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return jsonify(r.json()), r.status_code
    except requests.exceptions.RequestException as err:
        return jsonify({"error": "Apps Script nicht erreichbar", "details": str(err)}), 502


if __name__ == "__main__":
    # Render setzt PORT env-Var; fallback 10000
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
