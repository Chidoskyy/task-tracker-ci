#!/bin/bash
# start.sh: start Task Tracker in the background
# The output goes to a log file, so CodeDeploy does not wait for the program
LOG=/var/log/task-tracker.log
nohup python3 /opt/task-tracker/app.py > "$LOG" 2>&1 < /dev/null &
