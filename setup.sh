#!/bin/bash
cd "$(dirname "$0")"
PWD=$(pwd)

echo "Creating virtual environment..."
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

echo "installing service..."
sed -i "s|^ExecStart=.*|ExecStart=$PWD/run.sh|" wa-bot_server-mon.service
sudo ln -s $PWD/wa-bot_server-mon.service /etc/systemd/system/wa-bot_server-mon.service
sudo systemctl daemon-reload
sudo systemctl enable wa-bot_server-mon.service
sudo systemctl start wa-bot_server-mon.service
echo "Service installed and started."


