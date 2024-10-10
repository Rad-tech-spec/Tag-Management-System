#!/bin/bash

# Path to your Python script
SCRIPT="res_sarnia/src/main.py"

# Run the script in an infinite loop
while true; do
    # Check if the script is running
    if pgrep -f "$SCRIPT" > /dev/null; then
        echo "$SCRIPT is running..."
    else
        echo "$SCRIPT stopped. Restarting..."
        python3 "$SCRIPT" &  # Run the script in the background
    fi
    sleep 5  # Check every 5 seconds
done
