#!/bin/bash
cd "$(dirname "$0")"
PWD=$(pwd)

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    sudo ln -s $PWD/wa-bot_server-mon.service /etc/systemd/system/wa-bot_server-mon.service
    sudo systemctl daemon-reload
    sudo systemctl enable wa-bot_server-mon.service
    sudo systemctl start wa-bot_server-mon.service
    echo "Service installed and started."
fi

. venv/bin/activate
. set_env.prop.sh
python -u main.py