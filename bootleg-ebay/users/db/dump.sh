#!/bin/bash	
# Run this file when you want to "save" your current SQL state to git	
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )	
cd "$parent_path"	

docker exec -i $(docker-compose ps -q users-db) mysqldump -uroot -pbootleg users > sqlfile.sql	
