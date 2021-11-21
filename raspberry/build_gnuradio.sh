#!/usr/bin/sh
#Run crossplatform docker
docker run --privileged --rm docker/binfmt:a7996909642ee92942dcd6cff44b9b95f08dad64
#Create docker image. The packages will be built inside the container.
docker buildx build --platform linux/arm64  -t gnuradio-builder .
#Run docker image. 
docker run -v ${PWD}:/local --platform linux/arm64  -t gnuradio-builder

