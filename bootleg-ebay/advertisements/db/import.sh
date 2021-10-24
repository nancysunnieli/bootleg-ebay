#!/bin/bash
# Run this file when you did git pull to sync the latest changes into your SQL DBs
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

docker exec -i $(docker-compose ps -q advertisements-db) mysql -uroot -pbootleg advertisements < ./sqlfile.sql
