#!/bin/bash
# stop.sh: stop the running version of Task Tracker, if there is one
pkill -f "/opt/task-tracker/app.py" || true
