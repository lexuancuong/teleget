#!/bin/bash
docker stop teleget
docker rm teleget
docker build -t teleget:macos .
docker run -it -p 8000:8000 --name teleget --entrypoint bash --env-file=env -v $PWD:/srv/teleget -v $PWD/../logs:/srv/logs teleget:macos
