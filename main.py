from utils.util import get_wib_time, ping, format_time, print_log
from utils.config import CONFIG, DELAY, MSG, GREENAPI_API_KEY, GREENAPI_INSTANCES, MAX_RETRIES, SERVER_IP, CHAT_ID
from time import sleep
from whatsapp_api_client_python import API
import datetime

greenAPI = API.GreenAPI(GREENAPI_INSTANCES, GREENAPI_API_KEY)

is_down: bool = False
last_down_time: datetime.datetime = None
notification_sent: bool = False


def delay_ping(ip: str) -> bool:
    sleep(1)
    return not ping(ip)

print("====== SERVER MONITORING BOT ======")

while True:
    sleep(DELAY)

    # Verifikasi apakah server down dengan beberapa percobaan
    ping_results = [delay_ping(SERVER_IP) for _ in range(MAX_RETRIES)]
    print_log(f'pinging server at {format_time(get_wib_time())}')
    # Jika semua ping gagal, dianggap server DOWN
    all_ping_failed = all(ping_results)
    # Jika beberapa ping berhasil, dianggap server UP
    some_ping_successful = any([not x for x in ping_results])
    # jika beberapa ping gagal
    some_ping_failed = any(ping_results)

    if some_ping_failed and not all_ping_failed:
        print_log(f'network not stable, result {ping_results}')

    # Jika server down dan notifikasi belum dikirim
    if all_ping_failed and not is_down and not notification_sent:
        is_down = True
        notification_sent = True
        current_time = get_wib_time()
        last_down_time = current_time
        status_message = MSG.format(
            SERVER_IP, 'DOWN', format_time(current_time), "-")
        print_log(f'[DOWN] ping res {ping_results}')
        try:
            greenAPI.sending.sendMessage(CHAT_ID, status_message)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")

    # Jika server sudah kembali online setelah sebelumnya down
    elif some_ping_successful and is_down:
        is_down = False
        notification_sent = False
        current_time = get_wib_time()
        downtime = str(
            current_time - last_down_time) if last_down_time else "-"
        status_message = MSG.format(
            SERVER_IP, 'UP', format_time(current_time), downtime)
        print_log(f'[UP] ping res {ping_results}')
        try:
            greenAPI.sending.sendMessage(CHAT_ID, status_message)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")
        last_down_time = None

    # Menghindari spam notifikasi UP ketika server sudah dalam status UP
    if some_ping_successful and is_down and not notification_sent:
        notification_sent = False  # Reset notification_sent untuk pengiriman UP berikutnya
