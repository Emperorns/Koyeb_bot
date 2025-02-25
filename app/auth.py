import os

def authenticate(chat_id):
    allowed_id = os.getenv('ALLOWED_USER_ID')
    return str(chat_id) == allowed_id
