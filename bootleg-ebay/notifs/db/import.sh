#!/bin/bash
# Run this file when you did git pull to push the latest changes into your Mongo DBs
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

docker cp ./dump $(docker-compose ps -q notifs-db):/dump
docker exec -i $(docker-compose ps -q notifs-db) /usr/bin/mongorestore --username root --password bootleg --authenticationDatabase admin /dump