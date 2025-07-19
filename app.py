from flask import Flask, request
import requests, os
from utils import generate_gpt_response
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Verificación fallida", 403

    if request.method == "POST":
        data = request.get_json()
        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            user_msg = message["text"]["body"]
            sender_id = message["from"]
            response = generate_gpt_response(user_msg)

            send_whatsapp_message(sender_id, response)
        except Exception as e:
            print("Error:", e)

        return "OK", 200

def send_whatsapp_message(recipient, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=body)
    print("WhatsApp Response:", response.text)

if __name__ == "__main__":
    app.run(port=5000)
