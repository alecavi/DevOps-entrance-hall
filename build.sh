#!/bin/bash
docker rm entrance-hall --force
docker build -t entrance-hall .

docker run \
-d \
-p 80:80 \
--name entrance-hall \
--mount type=bind,source="$(pwd)/src",target="/home/src" \
entrance-hall

