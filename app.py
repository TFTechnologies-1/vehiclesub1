from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# -------------------
# Hardcoded API key
# -------------------
RAPIDAPI_KEY = "41298f856dmsh6ada35ec8b14548p14d735jsn78a502f80c1a"
BASE_URL = "https://rto-vehicle-information-india.p.rapidapi.com"

# -------------------
# Routes
# -------------------
@app.route("/", methods=["GET", "POST"])
def index():
    vehicle_data = None
    challan_data = None
    error_message = None

    if request.method == "POST":
        vehicle_no = request.form.get("vehicle_no", "").strip().upper()

        if not vehicle_no:
            error_message = "Please enter a vehicle number."
        else:
            # --- Step 1: Get Vehicle Info ---
            try:
                headers = {
                    "Content-Type": "application/json",
                    "x-rapidapi-host": "rto-vehicle-information-india.p.rapidapi.com",
                    "x-rapidapi-key": RAPIDAPI_KEY
                }
                payload = {
                    "vehicle_no": vehicle_no,
                    "consent": "Y",
                    "consent_text": "I hereby give my consent for KARMALabs to fetch my information"
                }

                vehicle_response = requests.post(f"{BASE_URL}/getVehicleInfo", json=payload, headers=headers)
                vehicle_json = vehicle_response.json()

                if vehicle_json.get("status"):
                    vehicle_data = vehicle_json.get("data")
                else:
                    error_message = vehicle_json.get("message", "Unable to fetch vehicle data.")

                # --- Step
