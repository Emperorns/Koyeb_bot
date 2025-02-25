import logging
import os

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('koyeb_bot.log'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logger initialized")
