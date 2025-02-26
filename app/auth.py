# app/auth.py
import os
import logging
from flask import request

def authenticate_request(req):
    """Verify if the incoming request is authorized."""
    try:
        # Log the incoming request for debugging
        logging.info(f"Incoming request: {req.json}")
        
        # Check if the request contains a valid update
        if 'message' not in req.json and 'edited_message' not in req.json:
            logging.warning("Request does not contain a 'message' or 'edited_message' key")
            return False
            
        # Extract the message object (either from 'message' or 'edited_message')
        message = req.json.get('message') or req.json.get('edited_message')
        
        # Get the chat ID from the message
        chat_id = message['chat']['id']
        
        # Get the allowed user ID from environment variables
        allowed_id = os.getenv('ALLOWED_USER_ID')
        
        # Verify if the chat ID matches the allowed user ID
        return str(chat_id) == allowed_id
        
    except KeyError as e:
        logging.error(f"Missing key in request: {e}")
        return False
    except Exception as e:
        logging.error(f"Authentication error: {e}")
        return False
