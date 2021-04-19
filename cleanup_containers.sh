for image in $(docker ps -a --format "{{.Names}}" | grep -v jupyter)
do
    docker rm $image
done
