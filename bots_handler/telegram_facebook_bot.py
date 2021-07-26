from flask import Flask, request, jsonify
from pymessenger.bot import Bot

from config import FACEBOOK_TOKEN, FACEBOOK_ID, TELEGRAM_INIT_WEBHOOK_URL, TELEGRAM_SEND_MESSAGE_URL

import requests

app = Flask(__name__)

bot = Bot(FACEBOOK_TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)

@app.route('/telegram', methods=['POST'])
def telegram():
    req = request.get_json()

    chat_id = req["message"]['chat']['id']
    incoming_message = req["message"]["text"]

    outgoing_message = incoming_message

    res = requests.get(TELEGRAM_SEND_MESSAGE_URL.format(chat_id, outgoing_message))

    success = True if res.status_code == 200 else False
    return jsonify(success=success)

@app.route("/facebook", methods=['GET'])
def autenticate():
    token_sent = request.args.get("hub.verify_token")    
    if token_sent == FACEBOOK_ID:
        return request.args.get("hub.challenge")
    return "FACEBOOK_ID incorrecto."

@app.route("/facebook", methods=['POST'])
def receive_message():
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response = message['message'].get('text')
                    bot.send_text_message(recipient_id, response)
        return "Mensaje recibido y procesado!"

if __name__ == '__main__':
    app.run(port='8000')


