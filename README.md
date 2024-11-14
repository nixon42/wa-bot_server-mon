# Server Monitoring Script

This is a Python-based server monitoring script that checks whether a specific server is up or down. If the server is down, the script sends a WhatsApp notification using the GreenAPI service. The script runs continuously in a loop, checking the server's status at regular intervals and notifying you if the status changes.

## Features
- Monitors server status via ICMP ping.
- Sends WhatsApp notifications when the server goes **UP** or **DOWN**.
- Keeps track of the downtime duration and displays it when the server comes back online.
- Runs continuously as a background service on Linux systems using **systemd**.

## Requirements

Before running this script, make sure you have the following dependencies installed:

- **Python 3.7+**
- **pip** (Python package manager)
- **Virtual environment** (`venv`)
- **GreenAPI** account and API keys
