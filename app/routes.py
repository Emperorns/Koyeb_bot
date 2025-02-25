from flask import Flask, request, jsonify
from app.auth import authenticate_request
from app.commands import handle_command
import logging

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not authenticate_request(request):
            logging.warning("Unauthorized webhook attempt")
            return jsonify({"status": "unauthorized"}), 403
            
        update = request.get_json()
        handle_command(update)
        return jsonify({"status": "processed"}), 200
        
    except Exception as e:
        logging.error(f"Webhook error: {str(e)}")
        return jsonify({"status": "error"}), 500
