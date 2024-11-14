from utils.util import get_wib_time, ping, format_time
from utils.config import CONFIG, DELAY, MSG, GREENAPI_API_KEY, GREENAPI_INSTANCES, MAX_RETRIES, SERVER_IP, CHAT_ID
from time import sleep
from whatsapp_api_client_python import API
import datetime

greenAPI = API.GreenAPI(GREENAPI_INSTANCES, GREENAPI_API_KEY)

is_down: bool = False
last_down_time: datetime.datetime = None
notification_sent: bool = False

print("====== SERVER MONITORING BOT ======")

while True:
    sleep(DELAY)

    # Verifikasi apakah server down dengan beberapa percobaan
    ping_results = [not ping(SERVER_IP) for _ in range(MAX_RETRIES)]
    # Jika semua ping gagal, dianggap server DOWN
    all_ping_failed = all(ping_results)
    # Jika semua ping berhasil, dianggap server UP
    all_ping_successful = not any(ping_results)


    # Jika server down dan notifikasi belum dikirim
    if all_ping_failed and not is_down and not notification_sent:
        is_down = True
        notification_sent = True
        current_time = get_wib_time()
        last_down_time = current_time
        status_message = MSG.format(
            SERVER_IP, 'DOWN', format_time(current_time), "-")
        try:
            greenAPI.sending.sendMessage(CHAT_ID, status_message)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")

    # Jika server sudah kembali online setelah sebelumnya down
    elif all_ping_successful and is_down:
        is_down = False
        notification_sent = False
        current_time = get_wib_time()
        downtime = str(
            current_time - last_down_time) if last_down_time else "-"
        status_message = MSG.format(
            SERVER_IP, 'UP', format_time(current_time), downtime)
        try:
            greenAPI.sending.sendMessage(CHAT_ID, status_message)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
        last_down_time = None

    # Menghindari spam notifikasi UP ketika server sudah dalam status UP
    if all_ping_successful and is_down and not notification_sent:
        notification_sent = False  # Reset notification_sent untuk pengiriman UP berikutnya
