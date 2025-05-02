#!/bin/bash
if ! dpkg -s python3.12-venv >/dev/null 2>&1; then
    sudo apt update
    sudo apt install python3.12-venv
fi

if [ ! -d "venv" ]; then
    echo "Starting up the virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if ! dpkg -s python3-pip >/dev/null 2>&1; then
    sudo apt update
    sudo apt install python3-pip
fi

if ! dpkg -s Flask >/dev/null 2>&1; then
    pip install Flask
fi

if ! dpkg -s requests >/dev/null 2>&1; then
    pip install requests
fi

python3 server/server.py &

while true; do
    python3 client/client.py
    sleep 1
done
