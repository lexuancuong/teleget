#!/bin/sh

python manage.py migrate

# Set container time
unlink /etc/localtime
ln -s /usr/share/zoneinfo/Universal /etc/localtime

while true; do
  echo "check pid app"
  ps -ef | grep -v grep | grep -i application
  if [ $? -ne "0" ]; then
    echo "Service started"
    python manage.py runserver 0.0.0.0:8000
    # Gunicorn 2n + 1 formula
    # gunicorn -w 3 --bind 0.0.0.0:80 app.wsgi:application
  else
    echo "Application not started !!! Please wait on 5 sec to restart"
  fi
  sleep 5
done
