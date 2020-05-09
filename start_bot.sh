#!/bin/bash
echo "Waiting 5s to start..."
sleep 5s
done=$(<done.txt)
while true; do
    if [ $(date +%a) == "Mo" && $done == "0" ]; then
        python3 myfreebot_cleanup.py
        sleep 1s
        echo "1" > done.txt
        reboot
    fi
    python3 myfreebot_v1.2.py
    sleep 2h
    if [ $(date +%a) == "Di" ]; then
        echo "0" > done.txt
    fi
done



