import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

app = Flask(__name__)

# Your bot token from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # Optional, if you want fixed chat_id
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route('/')
def home():
    return "🚀 KARMALabs RTO API is live!"

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        message_text = data.get("message", "")
        chat_id = data.get("chat_id", CHAT_ID)

        if not message_text or not chat_id:
            return jsonify({"error": "message and chat_id are required"}), 400

        payload = {
            "chat_id": chat_id,
            "text": message_text
        }
        resp = requests.post(TELEGRAM_API_URL, json=payload)

        if resp.status_code == 200:
            return jsonify({"status": "success", "message": message_text})
        else:
            return jsonify({"status": "failed", "error": resp.text}), 500

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

gunicorn
