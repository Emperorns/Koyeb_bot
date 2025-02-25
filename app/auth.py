import os
from flask import request

def authenticate_request(req):
    # Verify Telegram secret token
    if req.headers.get('X-Telegram-Secret') != os.getenv('TELEGRAM_WEBHOOK_SECRET'):
        return False
        
    # Verify allowed user ID
    chat_id = req.json.get('message', {}).get('chat', {}).get('id')
    return str(chat_id) == os.getenv('ALLOWED_USER_ID')
