import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from datetime import datetime
from pytz import timezone


def ping(host) -> bool:
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


def get_wib_time():
    """
    Return current time in WIB timezone or +7 GMT
    """
    jakarta_tz = timezone('Asia/Jakarta')
    wib_time = datetime.now(jakarta_tz)

    return wib_time


def format_time(time: datetime) -> str:
    """
    Format datetime object
    """
    return time.strftime("%Y-%m-%d %H:%M:%S")
