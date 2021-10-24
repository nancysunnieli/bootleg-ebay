#!/bin/bash
# Run this file when you did git pull to sync the latest changes into your SQL DB
docker exec -i $(docker-compose ps -q user-db) mysql -uroot -pbootleg users < ../bootleg-ebay/users/db/sqlfile.sql
docker exec -i $(docker-compose ps -q advertisement-db) mysql -uroot -pbootleg advertisements < ../bootleg-ebay/advertisements/db/sqlfile.sql
