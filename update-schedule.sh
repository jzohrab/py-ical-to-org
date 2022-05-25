#!/bin/bash
# ref https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/
PATH=/usr/local/bin:/usr/local/sbin:~/bin:/usr/bin:/bin:/usr/sbin:/sbin

python3 -m venv .venv
source .venv/bin/activate
python main.py
deactivate
