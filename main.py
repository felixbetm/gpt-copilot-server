import requests
from flask import Flask, request, jsonify

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby9KvlENfvkOndVAfcQrOdKtIwt_AlO8EzjQRdKLL5ZZjxqUL6rMg6nzxtHE2oAhnfO/exec"
TOKEN          = "8235"

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Copilot-Server läuft.", "status": "ok"})

@app.route("/sheet/write", methods=["POST"])
def write_sheet():
    data   = request.get_json(force=True)
    sheet  = data.get("sheet")
    rng    = data.get("range")
    values = data.get("values")

    if not (sheet and rng and values):
        return jsonify({"error": "sheet, range, values sind Pflicht"}), 400

    payload = {
        "token": TOKEN,
        "sheet": sheet,
        "range": rng,
        "values": values
    }
    # Weiterleitungen zulassen (Apps-Script 302)
    r = requests.post(APP_SCRIPT_URL, json=payload, allow_redirects=True, timeout=15)
    return jsonify(r.json()), r.status_code

@app.route("/sheet/read", methods=["GET"])
def read_sheet():
    sheet = request.args.get("sheet")
    rng   = request.args.get("range")
    if not (sheet and rng):
        return jsonify({"error": "sheet und range sind Pflicht"}), 400

    params = {
        "token": TOKEN,
        "sheet": sheet,
        "range": rng
    }
    r = requests.get(APP_SCRIPT_URL, params=params, allow_redirects=True, timeout=15)
    return jsonify(r.json()), r.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
