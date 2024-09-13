#!/bin/bash

# if [[ ! -z "DOCKERHUB_USER" ]]; then
#     read 
    
# fi

# echo $DOCKERHUB_USER

# Build of the images
# docker build -t augustodsgv/ffmpeg-backend ./backend
docker build -t augustodsgv/ffmpeg-frontend ./frontend

# # Checking if there is a docker container running the local image server
# if [  docker ps | grep -c "registry:2" -lt 1 ]; then
#     docker run -dp 5000:5000 --name image-local-repo registry:2
# fi

# # Giving local images the tag names of 
# docker tag ffmpeg-backend:latest localhost:5000/backend:latest
# docker tag ffmpeg-frontend:latest localhost:5000/frontend:latest

# docker push augustodsgv/ffmpeg-backend
docker push augustodsgv/ffmpeg-frontend

# docker pull augustodsgv/ffmpeg-backend
# docker pull augustodsgv/ffmpeg-frontend