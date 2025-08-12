from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Hardcoded RapidAPI credentials
API_URL = "https://rto-vehicle-information-india.p.rapidapi.com/getVehicleInfo"
API_KEY = "41298f856dmsh6ada35ec8b14548p14d735jsn78a502f80c1a"  # Replace if needed

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>KARMALabs - Vehicle Info Lookup</title>
</head>
<body>
    <h2>Vehicle Information Lookup</h2>
    <form method="POST">
        Vehicle Number: <input type="text" name="vehicle_no" required>
        <button type="submit">Search</button>
    </form>
    {% if data %}
        <h3>Result:</h3>
        <pre>{{ data }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    if request.method == "POST":
        vehicle_no = request.form["vehicle_no"]
        payload = {
            "vehicle_no": vehicle_no,
            "consent": "Y",
            "consent_text": "I hereby give my consent for KARMALabs API to fetch my information"
        }
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "rto-vehicle-information-india.p.rapidapi.com",
            "x-rapidapi-key": API_KEY
        }
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()
        except Exception as e:
            data = {"error": str(e)}
    return render_template_string(HTML_FORM, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
