#!/bin/bash
# Check if the script is already running
if pidof -o %PPID -x "$0"; then
    echo "Script is already running." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
    exit 1
else 
    echo "Script not running! Starting..." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
    
    # Long-running task
    while true; do
        echo "Job running." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
        if ! python3 /home/actemiumsumma/Historian-Sarnia/res_sarnia/src/main.py; then
            echo "Failed to start Python script." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
        fi
        sleep 300
    done
fi
