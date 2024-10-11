#!/bin/bash

# # Path to your Python script
# SCRIPT="res_sarnia/src/main.py"

# # Run the script in an infinite loop
# while true; do
#     # Check if the script is running
#     if pgrep -f "$SCRIPT" > /dev/null; then
#         echo "$SCRIPT is running..."
#     else
#         echo "$SCRIPT stopped. Restarting..."
#         python3 "$SCRIPT" &  # Run the script in the background
#     fi
#     sleep 5  # Check every 5 seconds
# done

# # Check if the cron job is running
# while true; do
#     if pidof -o %PPID -x "$0"; then
#         echo "Cron job is running."
#     else
#         echo "Cron job not running. Starting it..."
#         python3 res_sarnia/src/main.py &  # Replace with your cron job command
#     fi
#     sleep 300
# done

# Check if the script is already running
if pidof -o %PPID -x "$0"; then
    echo "Script is already running." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
    exit 1
else 
    echo "Script not running! Starting..." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
    # Long-running task
    while true; do
        echo "Job running." >> /home/actemiumsumma/Historian-Sarnia/crontaboutput.txt
        python3 res_sarnia/src/main.py & # Replace with your cron job command
        sleep 300
    done
fi