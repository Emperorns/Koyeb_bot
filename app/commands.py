# app/commands.py
import os
import logging
import requests
from app.koyeb_client import KoyebManager

koyeb = KoyebManager()

def handle_command(update):
    """Handle incoming Telegram commands."""
    try:
        message = update.get('message', {})
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        
        if not text or not chat_id:
            logging.warning("Invalid message format")
            return
            
        commands = text.split()
        if not commands:
            return
            
        cmd = commands[0].lower()
        
        if cmd == '/logs' and len(commands) > 1:
            logs = koyeb.get_logs(commands[1])
            send_telegram(chat_id, logs[:4000])
            
        elif cmd == '/redeploy' and len(commands) > 1:
            res = koyeb.redeploy(commands[1])
            send_telegram(chat_id, f"Redeploy: {res}")
            
        elif cmd == '/list_services':
            services = "\n".join(koyeb.services.keys())
            send_telegram(chat_id, f"Active Services:\n{services}")
            
    except Exception as e:
        logging.error(f"Command error: {str(e)}")
        send_telegram(chat_id, "Error processing command")

def send_telegram(chat_id, text):
    """Send a message via Telegram."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
            json={'chat_id': chat_id, 'text': str(text)}
        )
    except Exception as e:
        logging.error(f"Failed to send Telegram message: {str(e)}")
