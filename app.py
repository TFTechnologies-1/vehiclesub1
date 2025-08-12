import os
import requests
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

if not RAPIDAPI_KEY:
    raise RuntimeError("RAPIDAPI_KEY not set. Put it in a .env file or set env var in Render.")

app = Flask(__name__, template_folder='templates', static_folder='static')

RAPIDAPI_HOST = "rto-vehicle-information-india.p.rapidapi.com"

# Helper: try multiple endpoints for challans for compatibility
def fetch_challans(reg):
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    payload = {"vehicle_no": reg, "consent": "Y", "consent_text": "I hereby give my consent for KARMALabs to fetch my information"}
    # Try known possible endpoints in order
    endpoints = [
        "https://{host}/getVehicleChallans".format(host=RAPIDAPI_HOST),
        "https://{host}/getChallan".format(host=RAPIDAPI_HOST),
        "https://{host}/api/vehicle/challan".format(host=RAPIDAPI_HOST),
    ]
    for url in endpoints:
        try:
            # prefer POST (some endpoints require POST)
            r = requests.post(url, headers=headers, json=payload, timeout=12)
            if r.status_code == 200:
                data = r.json()
                # basic sanity check - must contain 'data' or be truthy
                if isinstance(data, dict) and data.get("status") is not None:
                    return data
                # sometimes returns list or dict
                return {"status": True, "data": data}
        except Exception:
            pass
    # fallback: empty result
    return {"status": False, "data": []}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    reg = request.form.get('regNumber', '').strip()
    if not reg:
        return render_template('index.html', error="Please enter a registration number.", reg=reg)

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    payload = {"vehicle_no": reg, "consent": "Y", "consent_text": "I hereby give my consent for KARMALabs to fetch my information"}

    rc_result = {}
    challan_result = {"status": False, "data": []}
    # Fetch RC / vehicle info (user-provided curl used POST /getVehicleInfo)
    try:
        rc_url = f"https://{RAPIDAPI_HOST}/getVehicleInfo"
        r = requests.post(rc_url, headers=headers, json=payload, timeout=12)
        if r.status_code == 200:
            rc_result = r.json()
        else:
            rc_result = {"status": False, "message": f"RC fetch failed: {r.status_code}"}
    except Exception as e:
        rc_result = {"status": False, "message": str(e)}

    # Fetch challans (try multiple endpoints)
    challan_result = fetch_challans(reg)

    # Compute total outstanding
    total = 0
    challans = []
    if challan_result.get("status") and challan_result.get("data"):
        challans = challan_result.get("data") or []
        # If data is a dict with nested list, try to find list
        if isinstance(challans, dict):
            # common pattern: {'data': [ ... ]}
            chal = challans.get("data") or []
            if isinstance(chal, list):
                challans = chal
        for c in challans:
            try:
                total += float(c.get("amount") or 0)
            except Exception:
                pass

    return render_template('index.html', rc=rc_result, challans=challans, total=total, reg=reg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
