# Setup 
```
$ docker run -d -p 3306:3306 --name mysql-docker-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=bdd -e MYSQL_USER=user -e MYSQL_PASSWORD=password mysql/mysql-server:latest
```
```
$ docker exec -it <docker ID> mysql -u root -p
```