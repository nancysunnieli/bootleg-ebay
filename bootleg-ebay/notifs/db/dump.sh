#!/bin/bash
# Run this file when you want to "save" your current MongoDB state to git
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

docker exec -i $(docker-compose ps -q notifs-db) rm -rf /dump
docker exec -i $(docker-compose ps -q notifs-db) /usr/bin/mongodump --username root --password bootleg --authenticationDatabase admin --out /dump
rm -rf ./dump
docker cp $(docker-compose ps -q notifs-db):/dump ./dump