import os
import json

with open('config.json', 'r') as f:
    CONFIG = json.load(f)

GREENAPI_INSTANCES = os.environ['GREENAPI_INSTANCE']
GREENAPI_API_KEY = os.environ['GREENAPI_API_KEY']
SERVER_IP = os.environ['SERVER_IP']
CHAT_ID = os.environ['CHAT_ID']
DELAY: float = CONFIG['delay_sec']
MAX_RETRIES: int = CONFIG['max_timeout_retry']

MSG = """
*******************************
    !!!!! NOTIFIKASI !!!!!     
*******************************

📍 *IP*         : {0}
🔧 *STATUS*     : {1}
⏰ *WAKTU*      : {2}
💤 *DOWN_TIME*  : {3}

------------------------------
"""
