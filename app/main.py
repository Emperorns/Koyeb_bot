import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from auth import authenticate
from logger import setup_logger
from koyeb_client import KoyebManager

app = Flask(__name__)
setup_logger()

# Initialize Koyeb Manager
koyeb = KoyebManager()

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(), None)
        chat_id = update.message.chat.id
        
        # Authentication check
        if not authenticate(chat_id):
            logging.warning(f"Unauthorized access attempt from {chat_id}")
            return jsonify(success=False), 403

        command = update.message.text.split()
        logging.info(f"Received command: {' '.join(command)} from {chat_id}")

        if command[0] == '/logs':
            if len(command) < 2:
                return send_message(chat_id, "Usage: /logs <account>")
            account = command[1]
            response = koyeb.get_logs(account)
            send_message(chat_id, response)

        elif command[0] == '/redeploy':
            if len(command) < 2:
                return send_message(chat_id, "Usage: /redeploy <account>")
            account = command[1]
            response = koyeb.redeploy(account)
            send_message(chat_id, response)

        elif command[0] == '/list_services':
            services = koyeb.list_services()
            send_message(chat_id, services)

        else:
            send_message(chat_id, "Unknown command")

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        send_message(chat_id, "⚠️ Error processing your request")
        return jsonify(success=False), 500

    return jsonify(success=True)

def send_message(chat_id, text):
    # Telegram message sending with error handling
    try:
        requests.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
            json={'chat_id': chat_id, 'text': text}
        )
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
