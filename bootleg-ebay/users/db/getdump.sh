#!/bin/bash
# Run this file when you want to "save" your current SQL state to git
docker exec -i $(docker-compose ps -q user-db) mysqldump -uroot -pbootleg users > sqlfile.sql
