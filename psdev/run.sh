export DOCKER_HOST="tcp://192.168.1.4:2375"
docker run --rm -it `docker build -q .`
