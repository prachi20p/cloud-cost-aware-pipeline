#!/bin/bash
cd ~/cloud-cost-aware-pipeline
git pull
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker run -d -p 80:80 -v $(pwd):/usr/share/nginx/html nginx
