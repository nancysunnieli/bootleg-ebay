# Helpful links

* https://realpython.com/python-mysql/
* https://realpython.com/python-mock-library/
* https://igeorgiev.eu/python/tdd/python-unittest-database-applications/
* https://www.w3schools.com/sql/sql_dates.asp


# APIs

* https://www.ibm.com/docs/ru/qradar-common?topic=overview-api-error-messages
* https://www.w3schools.com/python/ref_requests_response.asp
* https://medium.com/datasparq-technology/flask-api-exception-handling-with-custom-http-response-codes-c51a82a51a0f
* https://metamug.com/article/rest-api-naming-best-practices.html

# Commands


* To rebuild: `docker-compose up --build`
`docker-compose up -d users-db -d users-api`
`docker-compose up -d payments-db -d payments-api`
`docker-compose up -d auctions-db -d auctions-api `

`docker run --hostname mongodb --name mongo_xenial -p 28017:28017 -p 27017:27017 -e MONGODB_PASS="password" -d mongo:3.4-xenial`

`docker run --hostname mongodb --name mongo_latest -p 28017:28017 -p 27017:27017 -e MONGODB_PASS="password" -d mongo:latest`

`docker pull --platform linux/x86_64 mongo:latest`

Start mysql

```
docker exec -it 0dfc203c9d89 bash
mysql -uroot -pbootleg2 payments

```

# MongoDB issues for M1 Mac

https://githubmemory.com/repo/docker/for-mac/issues/5785
https://github.com/docker-library/mongo/issues/485#issuecomment-891991814
