# app/auth.py
import os
from flask import request

def authenticate_request():
    """Verify only allowed user can interact with the bot"""
    try:
        # Get chat ID from incoming request
        chat_id = request.json['message']['chat']['id']
        allowed_id = os.getenv('ALLOWED_USER_ID')
        
        return str(chat_id) == allowed_id
        
    except KeyError:
        # Missing required fields in request
        return False
