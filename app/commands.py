from app.koyeb_client import KoyebManager
import logging

koyeb = KoyebManager()

def handle_command(update):
    try:
        message = update.get('message', {})
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        
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
    import requests
    requests.post(
        f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage",
        json={'chat_id': chat_id, 'text': str(text)}
    )
