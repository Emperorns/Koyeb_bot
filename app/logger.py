import logging
import os
from datetime import datetime

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot_audit.log'),
            logging.StreamHandler()
        ]
    )
    logging.info("Logger initialized")
