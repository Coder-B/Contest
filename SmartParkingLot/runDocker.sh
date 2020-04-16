docker build --tag smartparkinglot:1.0 .
docker run --publish 80:8080 --detach --name SPL smartparkinglot:1.0