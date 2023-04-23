#!/bin/sh
#
# Set container time
unlink /etc/localtime
ln -s /usr/share/zoneinfo/Universal /etc/localtime

while true; do
  echo "check pid app"
  ps -ef | grep -v grep | grep -i main
  if [ $? -ne "0" ]; then
    echo "Service started"
    python3 /srv/crawler/main.py
  else
    echo "crawler not started !!! Please wait on 5 sec to restart"
  fi
  sleep 5
done
