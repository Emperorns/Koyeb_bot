# app/auth.py
import os
from flask import request

def authenticate_request(req):
    """
    Verify if the incoming request is authorized.
    
    Args:
        req: Flask request object containing the Telegram update
        
    Returns:
        bool: True if authorized, False otherwise
    """
    try:
        # Get the chat ID from the incoming request
        chat_id = req.json['message']['chat']['id']
        
        # Get the allowed user ID from environment variables
        allowed_id = os.getenv('ALLOWED_USER_ID')
        
        # Verify if the chat ID matches the allowed user ID
        return str(chat_id) == allowed_id
        
    except KeyError as e:
        # Log missing fields in the request
        print(f"Missing key in request: {e}")
        return False
        
    except Exception as e:
        # Log any other unexpected errors
        print(f"Authentication error: {e}")
        return False
